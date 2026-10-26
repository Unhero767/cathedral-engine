import json
import urllib.request

def trigger_comfyui_generation():
    url = "http://127.0.0.1:8188/prompt"
    prompt_payload = {
        "prompt": {
            "3": {
                "inputs": {
                    "seed": 4096,
                    "steps": 4,
                    "cfg": 1.0,
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
                    "ckpt_name": "flux1-schnell.safetensors"
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {
                    "width": 512,
                    "height": 768,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "text": "Cathedral-Engine Living Arcana tarot card key art, 32-bit HD-2D biomechanical gothic hard-noir aesthetic, fluid curvature silhouette, intricate sacred geometry, teal and gold spectral frequency, volumetric shadow attenuation, masterwork.",
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": "blurry, low quality, heavy muscular bulk, photorealistic human proportions, flat lighting",
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            }
        }
    }
    
    data = json.dumps(prompt_payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode("utf-8"))
        print(f"[+] ComfyUI Living Arcana generation queued successfully. Prompt ID: {result.get('prompt_id')}")
    except Exception as e:
        print(f"[!] ComfyUI connection error on port 8188: {e}")

if __name__ == "__main__":
    trigger_comfyui_generation()
