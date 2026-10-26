import json
import urllib.request
import time

def queue_prompt(prompt_payload):
    url = "http://127.0.0.1:8188/prompt"
    data = json.dumps({"prompt": prompt_payload}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode("utf-8"))
        return result.get('prompt_id')
    except Exception as e:
        print(f"[!] ComfyUI connection error on port 8188: {e}")
        return None

def build_workflow(seed, prefix, card_title, spectral_desc):
    return {
        "3": {
            "inputs": {
                "seed": seed,
                "steps": 40,
                "cfg": 6.8,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
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
                "ckpt_name": "dreamshaper_8.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {
            "inputs": {
                "width": 768,
                "height": 1152,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {
                "text": f"Cathedral-Engine Living Arcana tarot card key art {card_title}, 32-bit HD-2D biomechanical gothic hard-noir aesthetic, fluid curvature silhouette, {spectral_desc}, engraved filigree, high-contrast chiaroscuro lighting, intricate crosshatching shadows, volumetric shadow attenuation, masterwork.",
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {
                "text": "blurry, low quality, heavy muscular bulk, photorealistic human proportions, flat lighting, overexposed",
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
                "filename_prefix": prefix,
                "images": ["8", 0]
            },
            "class_type": "SaveImage"
        }
    }

# Queue Card 05
wf_05 = build_workflow(4100, "living_arcana_card_05", "Card 05 The Harmonic Scar Chamber", "violet and obsidian spectral frequency, paraconsistent state reconciliation")
pid_05 = queue_prompt(wf_05)
print(f"[+] Living Arcana Card #05 queued. Prompt ID: {pid_05}")

time.sleep(2)

# Queue Card 06
wf_06 = build_workflow(4101, "living_arcana_card_06", "Card 06 The Altar of the Sovereign Spark", "gold and crimson spectral frequency, foundational ignition and divine sovereignty")
pid_06 = queue_prompt(wf_06)
print(f"[+] Living Arcana Card #06 queued. Prompt ID: {pid_06}")

if __name__ == "__main__":
    print("[+] Batch inference queue submitted successfully.")
