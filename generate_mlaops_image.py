import urllib.request
import json
import uuid

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

prompt_workflow = {
    "3": {
        "inputs": {
            "seed": 42,
            "steps": 25,
            "cfg": 7.0,
            "sampler_name": "euler",
            "scheduler": "normal",
            "denoise": 1.0,
            "model": ["10", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["5", 0]
        },
        "class_type": "KSampler"
    },
    "4": {
        "inputs": {
            "ckpt_name": "dreamshaper_8.safetensors"
        },
        "class_type": "CheckpointLoaderSimple"
    },
    "5": {
        "inputs": {
            "width": 1024,
            "height": 1024,
            "batch_size": 1
        },
        "class_type": "EmptyLatentImage"
    },
    "6": {
        "inputs": {
            "text": "Cathedral-Engine interior sanctuary, gothic biomechanical architecture, hard-noir shadows, vibrant glowing runes, volumetric lighting, 32-bit HD-2D aesthetic, masterpiece, highly detailed",
            "clip": ["10", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "7": {
        "inputs": {
            "text": "blurry, low quality, distorted anatomy, modern elements",
            "clip": ["10", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "8": {
        "inputs": {
            "samples": ["3", 0],
            "vae": ["4", 2]
        },
        "class_type": "VAEDecode"
    },
    "9": {
        "inputs": {
            "filename_prefix": "MLAOS_Cathedral",
            "images": ["8", 0]
        },
        "class_type": "SaveImage"
    },
    "10": {
        "inputs": {
            "model": ["4", 0],
            "clip": ["4", 1],
            "lora_name": "mlaops_sdxl_lora_final.safetensors",
            "strength_model": 1.0,
            "strength_clip": 1.0
        },
        "class_type": "LoraLoader"
    }
}

def queue_prompt(workflow):
    data = {"prompt": workflow, "client_id": client_id}
    req = urllib.request.Request(
        f"http://{server_address}/prompt",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

print("[Σ-7] Queuing corrected MLAOS generation job with LoRA...")
res = queue_prompt(prompt_workflow)
print(f"[Σ-7] Prompt queued successfully. Response: {res}")
