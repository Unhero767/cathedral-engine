import urllib.request
import urllib.parse
import json
import time
import sqlite3
import hashlib

COMFY_URL = "http://127.0.0.1:8188/prompt"

def queue_prompt(prompt_workflow):
    data = json.dumps({"prompt": prompt_workflow}).encode('utf-8')
    req = urllib.request.Request(COMFY_URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[COMFY ERROR] Failed to connect to ComfyUI server at {COMFY_URL}: {e}")
        print("Ensure ComfyUI is running locally with '--listen' or default port 8188.")
        return None

def trigger_generation(prompt_text):
    # Minimal ComfyUI API workflow structure (Standard Text-to-Image / Flux / SDXL node layout)
    # You can substitute this with your exported ComfyUI API JSON workflow dictionary
    workflow = {
        "3": {
            "inputs": {
                "seed": int(time.time()),
                "steps": 20,
                "cfg": 7.0,
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
            "inputs": {"ckpt_name": "flux1-schnell.safetensors"},
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {
            "inputs": {"width": 1024, "height": 1024, "batch_size": 1},
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {
                "text": prompt_text,
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {
                "text": "text, watermark, low quality, deformed anatomy, heavy muscular bulk",
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
                "filename_prefix": "MLAOS_Cathedral_Gen",
                "images": ["8", 0]
            },
            "class_type": "SaveImage"
        }
    }

    print(f"[COMFY BRIDGE] Dispatching generation request...")
    print(f" -> Prompt: {prompt_text}")
    
    response = queue_prompt(workflow)
    if response:
        prompt_id = response.get("prompt_id")
        print(f"[COMFY BRIDGE] Generation queued successfully. Prompt ID: {prompt_id}")
        
        # Log to Ash Archive
        conn = sqlite3.connect("ash_archive.db")
        cursor = conn.cursor()
        timestamp = time.time()
        payload = f"COMFY_GENERATION: {prompt_text}"
        cursor.execute("SELECT current_hash FROM ash_ledger ORDER BY id DESC LIMIT 1;")
        row = cursor.fetchone()
        parent_hash = row[0] if row else "0" * 64
        current_hash = hashlib.sha256(f"{timestamp}{payload}{parent_hash}".encode()).hexdigest()
        
        cursor.execute('''
            INSERT INTO ash_ledger (timestamp, node_type, state_payload, parent_hash, current_hash)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, "ASSET_GENERATION", payload, parent_hash, current_hash))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    import sys
    custom_prompt = sys.argv[1] if len(sys.argv) > 1 else "Dark gothic cathedral interior, fluid curvature architecture, dramatic chiaroscuro lighting, volumetric light shafts, intricate stone carvings, 32-bit HD-2D aesthetic."
    trigger_generation(custom_prompt)
