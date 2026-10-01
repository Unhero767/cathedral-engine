import os
import torch
from accelerate import Accelerator
from diffusers import AutoencoderKL, DDPMScheduler, UNet2DConditionModel
from peft import LoraConfig, get_peft_model
from transformers import AutoTokenizer, CLIPTextModel, CLIPTextModelWithProjection
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

# Configuration Constants
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
DATASET_DIR = "./dataset/20_mlaostyle"
OUTPUT_DIR = "./output/mlaostyle_lora"
RESOLUTION = 1024
BATCH_SIZE = 1  # Reduced to 1 for Apple Silicon unified memory optimization on MPS
LEARNING_RATE = 1e-4

class MLAOSDataset(Dataset):
    def __init__(self, data_dir, resolution=1024):
        self.data_dir = data_dir
        self.image_files = [f for f in os.listdir(data_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.transform = transforms.Compose([
            transforms.Resize((resolution, resolution), interpolation=transforms.InterpolationMode.BILINEAR),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_name = self.image_files[idx]
        img_path = os.path.join(self.data_dir, img_name)
        image = Image.open(img_path).convert("RGB")
        tensor = self.transform(image)
        caption = "MLAOS-Prime CC-Ω lithographic style, dark gothic obsidian and hyper-detailed biomechanical architecture"
        return {"pixel_values": tensor, "caption": caption}

def main():
    # Note: On Apple Silicon MPS, use float32 or let autocast handle precision to avoid half-precision NaN issues
    accelerator = Accelerator(gradient_accumulation_steps=4, mixed_precision="no")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"[*] Initializing SDXL LoRA Training Pipeline on: {accelerator.device}")
    
    # Check for Hugging Face token to avoid rate limits
    hf_token = os.environ.get("HF_TOKEN", None)
    if hf_token:
        print("[*] Hugging Face token detected.")
    else:
        print("[!] Warning: HF_TOKEN not set. Set export HF_TOKEN='your_token' if you hit rate limits.")

    tokenizer_one = AutoTokenizer.from_pretrained(MODEL_ID, subfolder="tokenizer", token=hf_token)
    tokenizer_two = AutoTokenizer.from_pretrained(MODEL_ID, subfolder="tokenizer_2", token=hf_token)
    text_encoder_one = CLIPTextModel.from_pretrained(MODEL_ID, subfolder="text_encoder", torch_dtype=torch.float32, token=hf_token)
    text_encoder_two = CLIPTextModelWithProjection.from_pretrained(MODEL_ID, subfolder="text_encoder_2", torch_dtype=torch.float32, token=hf_token)
    
    vae = AutoencoderKL.from_pretrained(MODEL_ID, subfolder="vae", torch_dtype=torch.float32, token=hf_token)
    unet = UNet2DConditionModel.from_pretrained(MODEL_ID, subfolder="unet", torch_dtype=torch.float32, token=hf_token)

    vae.requires_grad_(False)
    text_encoder_one.requires_grad_(False)
    text_encoder_two.requires_grad_(False)
    unet.requires_grad_(False)

    lora_config = LoraConfig(
        r=32,
        lora_alpha=32,
        target_modules=["to_k", "to_q", "to_v", "to_out.0"],
        lora_dropout=0.0,
        bias="none",
    )
    unet = get_peft_model(unet, lora_config)
    unet.print_trainable_parameters()

    dataset = MLAOSDataset(DATASET_DIR, RESOLUTION)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)

    optimizer = torch.optim.AdamW(
        [p for p in unet.parameters() if p.requires_grad],
        lr=LEARNING_RATE,
        betas=(0.9, 0.999),
        weight_decay=1e-2,
        eps=1e-8,
    )

    unet, optimizer, dataloader = accelerator.prepare(unet, optimizer, dataloader)
    noise_scheduler = DDPMScheduler.from_pretrained(MODEL_ID, subfolder="scheduler", token=hf_token)

    # Move frozen models to device
    text_encoder_one.to(accelerator.device)
    text_encoder_two.to(accelerator.device)
    vae.to(accelerator.device)

    global_step = 0
    unet.train()

    for epoch in range(50):
        for step, batch in enumerate(dataloader):
            with accelerator.accumulate(unet):
                pixel_values = batch["pixel_values"].to(accelerator.device, dtype=torch.float32)
                
                with torch.no_grad():
                    latents = vae.encode(pixel_values).latent_dist.sample()
                    latents = latents * vae.config.scaling_factor

                noise = torch.randn_like(latents)
                bsz = latents.shape[0]
                timesteps = torch.randint(0, noise_scheduler.config.num_train_timesteps, (bsz,), device=latents.device).long()
                noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)

                inputs_one = tokenizer_one(batch["caption"], padding="max_length", max_length=70, truncation=True, return_tensors="pt").input_ids.to(accelerator.device)
                inputs_two = tokenizer_two(batch["caption"], padding="max_length", max_length=70, truncation=True, return_tensors="pt").input_ids.to(accelerator.device)
                
                with torch.no_grad():
                    encoder_output_one = text_encoder_one(inputs_one, output_hidden_states=True)
                    prompt_embeds_one = encoder_output_one.hidden_states[-2]
                    encoder_output_two = text_encoder_two(inputs_two, output_hidden_states=True)
                    prompt_embeds_two = encoder_output_two.hidden_states[-2]
                    pooled_prompt_embeds = encoder_output_two[0]
                    prompt_embeds = torch.cat([prompt_embeds_one, prompt_embeds_two], dim=-1)

                add_time_ids = torch.tensor([[RESOLUTION, RESOLUTION, 0, 0, RESOLUTION, RESOLUTION]], device=latents.device, dtype=torch.float32).repeat(bsz, 1)
                added_cond_kwargs = {"text_embeds": pooled_prompt_embeds, "time_ids": add_time_ids}

                model_pred = unet(noisy_latents, timesteps, prompt_embeds, added_cond_kwargs=added_cond_kwargs).sample

                loss = torch.nn.functional.mse_loss(model_pred.float(), noise.float(), reduction="mean")
                accelerator.backward(loss)
                
                optimizer.step()
                optimizer.zero_grad()

            global_step += 1
            if global_step % 5 == 0:
                print(f"Epoch {epoch} | Step {global_step} | Loss: {loss.detach().item():.4f}")

        unwrapped_unet = accelerator.unwrap_model(unet)
        unwrapped_unet.save_pretrained(os.path.join(OUTPUT_DIR, f"checkpoint_epoch_{epoch}"))

    print(f"[*] Training complete. LoRA saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
