import json

# Programmatically build standard ComfyUI API nodes (CheckpointLoader, CLIPTextEncode, Sampler, VAEEncode/Decode, SaveImage)
workflow = {
    "3": {
        "inputs": {
            "seed": 42,
            "steps": 20,
            "cfg": 8.0,
            "sampler_name": "euler",
            "scheduler": "normal",
            "denoise": 1.0,
            "model": ["4", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["5", 0]
        },
        "class_type": "KSampler"
    },
    "4": {
        "inputs": {
            "ckpt_name": "v1-5-pruned-emaonly.safetensors" # Replace with your local checkpoint model name
        },
        "class_type": "CheckpointLoaderSimple"
    },
    "5": {
        "inputs": {
            "width": 512,
            "height": 512,
            "batch_size": 1
        },
        "class_type": "EmptyLatentImage"
    },
    "6": {
        "inputs": {
            "text": "Dark cybernetic aesthetic, monolithic geometry, high contrast",
            "clip": ["4", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "7": {
        "inputs": {
            "text": "text, watermark, low quality",
            "clip": ["4", 1]
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
            "filename_prefix": "terminal_gen",
            "images": ["8", 0]
        },
        "class_type": "SaveImage"
    }
}

with open("workflow_api.json", "w", encoding="utf-8") as f:
    json.dump(workflow, f, indent=4)

print("workflow_api.json successfully generated via terminal.")
