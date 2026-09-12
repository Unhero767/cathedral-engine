import json
import urllib.request
import urllib.parse
import time
import os
import hashlib
from PIL import Image

def generate_via_comfyui(prompt, negative_prompt="blurry, low quality", host="127.0.0.1:8188", checkpoint="flux1-dev.safetensors"):
    # Standard ComfyUI prompt workflow payload
    workflow = {
        "3": {"class_type": "KSampler", "inputs": {"seed": int(time.time()), "steps": 20, "cfg": 7.0, "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": checkpoint}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip":}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": negative_prompt, "clip":}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae":}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "Cathedral_Chamber", "images": ["8", 0]}}
    }
    
    data = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(f"http://{host}/prompt", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5.0) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f"[+] ComfyUI Prompt Queued. Prompt ID: {res.get('prompt_id')}")

if __name__ == "__main__":
    from synthesize_chamber_artifact import MythicPromptCompiler
    compiler = MythicPromptCompiler()
    pos, neg, seed, cfg, _ = compiler.compile(5, 0.12, 1.45, 0.92, "THETA_GOLD")
    generate_via_comfyui(pos, neg)
