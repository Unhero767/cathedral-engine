import os
import time
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from accelerate import Accelerator
from diffusers import StableDiffusionXLPipeline
from peft import LoraConfig, get_peft_model
from tqdm import tqdm

class CathedralDataset(Dataset):
    def __init__(self, data_dir, tokenizer_1, tokenizer_2, size=1024):
        self.image_paths = []
        self.captions = []
        print(f"[Dataset] Scanning directory: {data_dir}")
        for root, _, files in os.walk(data_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    img_path = os.path.join(root, file)
                    txt_path = os.path.splitext(img_path)[0] + ".txt"
                    if os.path.exists(txt_path):
                        with open(txt_path, 'r', encoding='utf-8') as f:
                            caption = f.read().strip()
                        self.image_paths.append(img_path)
                        self.captions.append(caption)
        
        print(f"[Dataset] Loaded {len(self.image_paths)} valid image-caption pairs.")
        
        self.transform = transforms.Compose([
            transforms.Resize((size, size), interpolation=transforms.InterpolationMode.BILINEAR),
            transforms.CenterCrop(size),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5]),
        ])
        self.tokenizer_1 = tokenizer_1
        self.tokenizer_2 = tokenizer_2

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")
        pixel_values = self.transform(image)
        caption = self.captions[idx]
        
        inputs_1 = self.tokenizer_1(caption, padding="max_length", max_length=77, truncation=True, return_tensors="pt")
        inputs_2 = self.tokenizer_2(caption, padding="max_length", max_length=77, truncation=True, return_tensors="pt")
        
        return {
            "pixel_values": pixel_values,
            "input_ids_1": inputs_1.input_ids[0],
            "input_ids_2": inputs_2.input_ids[0]
        }

def main():
    accelerator = Accelerator(mixed_precision="bf16")
    print(f"[Hardware] Accelerator initialized. Device: {accelerator.device} | Mixed Precision: bf16")
    
    model_path = "/users/kennethdallmier/cathedral_engine/models/sdxl_base.safetensors"
    dataset_dir = "/users/kennethdallmier/cathedral_engine/dataset"
    output_dir = "/users/kennethdallmier/cathedral_engine/output"
    os.makedirs(output_dir, exist_ok=True)

    print(f"[Model] Loading SDXL base checkpoint from: {model_path}")
    pipeline = StableDiffusionXLPipeline.from_single_file(
        model_path, 
        torch_dtype=torch.bfloat16
    )
    
    unet = pipeline.unet
    vae = pipeline.vae
    text_encoder_1 = pipeline.text_encoder
    text_encoder_2 = pipeline.text_encoder_2
    tokenizer_1 = pipeline.tokenizer
    tokenizer_2 = pipeline.tokenizer_2
    scheduler = pipeline.scheduler

    vae.requires_grad_(False)
    text_encoder_1.requires_grad_(False)
    text_encoder_2.requires_grad_(False)
    print("[Model] Base components frozen (VAE & Text Encoders).")
    
    lora_config = LoraConfig(
        r=32,
        lora_alpha=16,
        target_modules=["to_k", "to_q", "to_v", "to_out.0"],
        lora_dropout=0.0,
        bias="none"
    )
    unet = get_peft_model(unet, lora_config)
    unet.print_trainable_parameters()

    dataset = CathedralDataset(dataset_dir, tokenizer_1, tokenizer_2)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True, num_workers=2)

    optimizer = torch.optim.AdamW8bit(unet.parameters(), lr=1e-4)

    unet, optimizer, dataloader = accelerator.prepare(unet, optimizer, dataloader)
    vae.to(accelerator.device, dtype=torch.bfloat16)
    text_encoder_1.to(accelerator.device, dtype=torch.bfloat16)
    text_encoder_2.to(accelerator.device, dtype=torch.bfloat16)

    global_step = 0
    epochs = 10
    total_steps = len(dataloader) * epochs

    print(f"\n[Training] Starting loop | Epochs: {epochs} | Total Steps: {total_steps}\n" + "="*50)

    for epoch in range(epochs):
        unet.train()
        epoch_start_time = time.time()
        progress_bar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{epochs}", disable=not accelerator.is_main_process)
        
        epoch_loss = 0.0
        for step, batch in enumerate(progress_bar):
            with torch.no_grad():
                latents = vae.encode(batch["pixel_values"].to(accelerator.device, dtype=torch.bfloat16)).latent_dist.sample()
                latents = latents * vae.config.scaling_factor

                encoder_output_1 = text_encoder_1(batch["input_ids_1"].to(accelerator.device), output_hidden_states=True)
                text_embeds_1 = encoder_output_1.hidden_states[-2]
                
                encoder_output_2 = text_encoder_2(batch["input_ids_2"].to(accelerator.device), output_hidden_states=True)
                text_embeds_2 = encoder_output_2.hidden_states[-2]
                pooled_embeds = encoder_output_2[0]

                prompt_embeds = torch.cat([text_embeds_1, text_embeds_2], dim=-1)

                noise = torch.randn_like(latents)
                timesteps = torch.randint(0, scheduler.config.num_train_steps, (latents.shape[0],), device=latents.device).long()
                noisy_latents = scheduler.add_noise(latents, noise, timesteps)

                add_time_ids = torch.tensor([[1024, 1024, 0, 0, 1024, 1024]] * latents.shape[0], dtype=torch.bfloat16, device=accelerator.device)
                
                added_cond_kwargs = {
                    "text_embeds": pooled_embeds,
                    "time_ids": add_time_ids
                }

                model_pred = unet(noisy_latents, timesteps, prompt_embeds, added_cond_kwargs=added_cond_kwargs).sample

                if scheduler.config.prediction_type == "epsilon":
                    target = noise
                elif scheduler.config.prediction_type == "v_prediction":
                    target = scheduler.get_v_prediction(latents, noise, timesteps)
                else:
                    raise ValueError(f"Unknown prediction type {scheduler.config.prediction_type}")

                loss = torch.nn.functional.mse_loss(model_pred.float(), target.float(), reduction="mean")

            accelerator.backward(loss)
            optimizer.step()
            optimizer.zero_grad()

            global_step += 1
            epoch_loss += loss.item()
            
            progress_bar.set_postfix({"loss": f"{loss.item():.4f}", "step": global_step})

        epoch_duration = time.time() - epoch_start_time
        avg_epoch_loss = epoch_loss / len(dataloader)
        print(f"[Epoch Complete] Epoch {epoch+1} finished in {epoch_duration:.2f}s | Average Loss: {avg_epoch_loss:.4f}")

        if accelerator.is_main_process:
            unwrapped_unet = accelerator.unwrap_model(unet)
            ckpt_path = os.path.join(output_dir, f"epoch_{epoch+1}")
            unwrapped_unet.save_pretrained(ckpt_path)
            print(f"[Checkpoint] Saved LoRA weights to {ckpt_path}\n" + "-"*50)

    print("[Training] Pipeline execution completed successfully.")

if __name__ == "__main__":
    main()
