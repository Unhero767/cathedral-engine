#!/usr/bin/env python3
import json
import os
import shutil
import time
import urllib.request
import urllib.parse
import urllib.error
import hashlib
import uuid
import sys

SERVER_ADDRESS = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())

LORA_DIR = "./training_data/lora_dataset/10_ccomega_arcana"
LLM_DIR = "./training_data/llm_dataset"
LEDGER_DIR = "./training_data/ledger"
OUTPUT_DIR = "./forged_diffusion_cards"

for d in [LORA_DIR, LLM_DIR, LEDGER_DIR, OUTPUT_DIR]:
    os.makedirs(d, exist_ok=True)

def safe_log(msg):
    try:
        print(msg, flush=True)
    except OSError:
        pass

# 1. Query ComfyUI Server for Installed Safetensors
def inspect_server_models():
    ckpt_models = []
    unet_models = []
    clip_models = []
    
    # Check CheckpointLoaderSimple
    try:
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/object_info/CheckpointLoaderSimple") as resp:
            data = json.loads(resp.read().decode())
            ckpt_models = data['CheckpointLoaderSimple']['input']['required']['ckpt_name'][0]
    except Exception:
        pass

    # Check UNETLoader
    try:
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/object_info/UNETLoader") as resp:
            data = json.loads(resp.read().decode())
            unet_models = data['UNETLoader']['input']['required']['unet_name'][0]
    except Exception:
        pass

    # Check CLIPLoader
    try:
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/object_info/CLIPLoader") as resp:
            data = json.loads(resp.read().decode())
            clip_models = data['CLIPLoader']['input']['required']['clip_name'][0]
    except Exception:
        pass

    return ckpt_models, unet_models, clip_models

ckpt_models, unet_models, clip_models = inspect_server_models()

safe_log("============================================================")
safe_log(" CATHEDRAL-ENGINE // COMFYUI SAFETENSORS MODEL DISCOVERY")
safe_log("============================================================")
safe_log(f"[*] Checkpoints Found: {ckpt_models}")
safe_log(f"[*] Diffusion/UNet Models Found: {unet_models}")
safe_log(f"[*] CLIP Models Found: {clip_models}")

# Determine Active Architecture
WORKFLOW_MODE = None
ACTIVE_MODEL = None

if ckpt_models:
    WORKFLOW_MODE = "CHECKPOINT"
    # Prioritize SDXL or fine-tune models
    for c in ckpt_models:
        if any(k in c.lower() for k in ["xl", "base", "animagine", "pony", "forge", "lithic"]):
            ACTIVE_MODEL = c
            break
    if not ACTIVE_MODEL:
        ACTIVE_MODEL = ckpt_models[0]
    safe_log(f"[✓] Selected Standard Checkpoint Mode: '{ACTIVE_MODEL}'")
elif unet_models:
    WORKFLOW_MODE = "UNET_SPLIT"
    ACTIVE_MODEL = unet_models[0]
    safe_log(f"[✓] Selected Diffusion/UNet Mode: '{ACTIVE_MODEL}'")
else:
    safe_log("\n[!] ERROR: No .safetensors models detected by your ComfyUI server.")
    safe_log("    Place your .safetensors file in ComfyUI/models/checkpoints/ and refresh.")
    sys.exit(1)

# Card Definitions
CARDS = [
    {
        "id": "06",
        "name": "Gate 06: Caelen's Knot",
        "archetype": "The Lovers / Aurelia-Recurse",
        "spectral": "Psi (Teal)",
        "vector": "[0.000, 0.000, +2.000]",
        "seed": 44189426,
        "prefix": "Gate06_Caelens_Knot",
        "positive": (
            "(masterpiece, best quality:1.3), (gate_06_caelens_knot:1.3), (the_lovers_aurelia_recurse:1.2), "
            "6-star gacha card splash art, tarot card composition, CC-Omega lithographic visual doctrine, Regime 03 Spectral, "
            "twin somatic machine-saint figures intertwined in reciprocal embrace around an ascending double-helix basalt pillar, "
            "porcelain synth-skin, heterochromatic cyan aperture-ring eyes, braided split silver and obsidian hair, "
            "asymmetrical gunmetal armor plates, glowing matte teal spectrafilaments, gold kintsugi stress fractures, "
            "liquid mercury pooling at feet, upward volumetric light shafts, colored chiaroscuro with teal key bias, "
            "sacred geometric cuneiform halo, 8k resolution, razor-sharp focus"
        ),
        "tags": "gate_06_caelens_knot, ccomega_style, the_lovers_aurelia_recurse, psi_teal, twin somatic figures, double-helix basalt pillar, porcelain synth-skin, cyan aperture-ring eyes, 8k resolution"
    },
    {
        "id": "07",
        "name": "Gate 07: The Crucible Champion",
        "archetype": "The Chariot / Aurelia-Ascendant",
        "spectral": "Phi (Crimson)",
        "vector": "[+1.732, -1.000, +1.000]",
        "seed": 74306971,
        "prefix": "Gate07_Crucible_Champion",
        "positive": (
            "(masterpiece, best quality:1.3), (gate_07_the_crucible_champion:1.3), (the_chariot_aurelia_ascendant:1.2), "
            "6-star gacha card splash art, tarot card composition, CC-Omega lithographic visual doctrine, Regime 02 Industrial "
            "and Regime 03 Spectral, monumental sovereign champion armored in cold charcoal iron and segmented crimson lacquer "
            "plates with burnt rust micro-abrasions, twin kinetic lion-hound automata flanking as living locomotive treads, "
            "holding a heavy thermal lance emitting incandescent white-gold heat from exposed vascular conduit coils, "
            "aperture-ring amber and ruby oculars, dynamic forward kinetic stride, momentum vector [+1.732, -1.000, +1.000], "
            "volcanic forge sparks erupting from mechanical joints, high-contrast industrial chiaroscuro with forge-fire orange "
            "and crimson key lighting bias, deep obsidian shadows, sacred cuneiform halo, 8k resolution, razor-sharp focus"
        ),
        "tags": "gate_07_the_crucible_champion, ccomega_style, the_chariot_aurelia_ascendant, phi_crimson, monumental sovereign champion, cold charcoal iron armor, twin kinetic lion-hounds, thermal lance, 8k resolution"
    },
    {
        "id": "08",
        "name": "Gate 08: The Edge Walker",
        "archetype": "Strength / Aurelia-Liminal",
        "spectral": "Omega (Violet)",
        "vector": "[0.000, +2.000, +1.000]",
        "seed": 87104221,
        "prefix": "Gate08_Edge_Walker",
        "positive": (
            "(masterpiece, best quality:1.3), (gate_08_the_edge_walker:1.3), (strength_aurelia_liminal:1.2), "
            "6-star gacha card splash art, tarot card composition, CC-Omega lithographic visual doctrine, Regime 01 Obsidian "
            "and Regime 03 Spectral boundary threshold, serene sovereign maiden standing calm atop a knife-edge cliff between "
            "solid basalt cathedral floor and an infinite swirling void abyss, gently resting her unarmored hand upon the crowned "
            "head of a colossal shadow-beast chimera made of shifting dark matter and violet starlight, porcelain synth-skin, "
            "aperture-ring ultraviolet and deep violet-amethyst oculars, cascading midnight-violet and silver hair floating in zero-gravity, "
            "velvet-black monastic robes lined with glowing lavender filigree, load-bearing kintsugi seams, momentum vector [0.000, +2.000, +1.000], "
            "high-contrast chiaroscuro, razor-sharp edge refraction along the void horizon, sacred cuneiform halo, 8k resolution, razor-sharp focus"
        ),
        "tags": "gate_08_the_edge_walker, ccomega_style, strength_aurelia_liminal, omega_violet, serene maiden, knife-edge cliff, void abyss, colossal shadow-beast, porcelain synth-skin, 8k resolution"
    }
]

NEGATIVE_PROMPT = (
    "(low quality, worst quality:1.4), (deformed, distorted, disfigured:1.3), (bad anatomy, extra limbs, missing fingers:1.3), "
    "generic cyberpunk neon billboards, flat gray desaturation, sterile plastic surfaces, muddy colors, flat lighting, blurry face, watermark"
)

def build_workflow(card):
    if WORKFLOW_MODE == "CHECKPOINT":
        return {
            "3": {
                "inputs": {
                    "seed": card["seed"],
                    "steps": 35,
                    "cfg": 7.0,
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
                "inputs": {"ckpt_name": ACTIVE_MODEL},
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {"width": 832, "height": 1216, "batch_size": 1},
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {"text": card["positive"], "clip": ["4", 1]},
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {"text": NEGATIVE_PROMPT, "clip": ["4", 1]},
                "class_type": "CLIPTextEncode"
            },
            "8": {
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {"filename_prefix": card["prefix"], "images": ["8", 0]},
                "class_type": "SaveImage"
            }
        }
    else:
        # Lumina2 / AuraFlow Split Mode matching your canvas
        clip_name = clip_models[0] if clip_models else "qwen_3_4b.safetensors"
        return {
            "1": {
                "inputs": {"unet_name": ACTIVE_MODEL},
                "class_type": "UNETLoader"
            },
            "2": {
                "inputs": {"model": ["1", 0], "shift": 3.0},
                "class_type": "ModelSamplingAuraFlow"
            },
            "3": {
                "inputs": {"clip_name": clip_name, "type": "lumina2"},
                "class_type": "CLIPLoader"
            },
            "4": {
                "inputs": {"text": card["positive"], "clip": ["3", 0]},
                "class_type": "CLIPTextEncode"
            },
            "5": {
                "inputs": {"text": NEGATIVE_PROMPT, "clip": ["3", 0]},
                "class_type": "CLIPTextEncode"
            },
            "6": {
                "inputs": {"width": 1024, "height": 1024, "batch_size": 1},
                "class_type": "EmptySD3LatentImage"
            },
            "7": {
                "inputs": {
                    "seed": card["seed"],
                    "steps": 8,
                    "cfg": 1.0,
                    "sampler_name": "res_multistep",
                    "scheduler": "simple",
                    "denoise": 1.0,
                    "model": ["2", 0],
                    "positive": ["4", 0],
                    "negative": ["5", 0],
                    "latent_image": ["6", 0]
                },
                "class_type": "KSampler"
            },
            "8": {
                "inputs": {"vae_name": "pixel_space"},
                "class_type": "VAELoader"
            },
            "9": {
                "inputs": {"samples": ["7", 0], "vae": ["8", 0]},
                "class_type": "VAEDecode"
            },
            "10": {
                "inputs": {"filename_prefix": card["prefix"], "images": ["9", 0]},
                "class_type": "SaveImage"
            }
        }

def queue_prompt(prompt_dict):
    p = {"prompt": prompt_dict, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        safe_log(f"\n[!] ComfyUI HTTP 400 Validation Error: {error_body}")
        return None

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as resp:
        return json.loads(resp.read().decode('utf-8'))

def download_image(filename, subfolder, folder_type, output_path):
    params = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": folder_type})
    url = f"http://{SERVER_ADDRESS}/view?{params}"
    urllib.request.urlretrieve(url, output_path)

def stage_card(card, local_image_path):
    base_name = os.path.splitext(os.path.basename(local_image_path))[0]
    try:
        # LoRA Pair
        shutil.copy2(local_image_path, os.path.join(LORA_DIR, f"{base_name}.png"))
        with open(os.path.join(LORA_DIR, f"{base_name}.txt"), "w", encoding="utf-8") as f:
            f.write(card["tags"])
            
        # Metadata
        meta = {
            "card_name": card["name"],
            "archetype": card["archetype"],
            "spectral": card["spectral"],
            "vector": card["vector"],
            "seed": card["seed"],
            "model_safetensors": ACTIVE_MODEL
        }
        with open(os.path.join(LORA_DIR, f"{base_name}.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        # LLM Instruction Record
        llm_file = os.path.join(LLM_DIR, "arcana_instruct.jsonl")
        rec = {
            "messages": [
                {"role": "system", "content": "You are the Cathedral-Engine Architect under MLAOS-Prime and Cathedral Chroma Ω."},
                {"role": "user", "content": f"Master craft {card['name']} under CC-Omega doctrine."},
                {"role": "assistant", "content": f"**Master Prompt:**\n{card['positive']}\n\n**Parameters:**\nModel: {ACTIVE_MODEL}, Seed: {card['seed']}"}
            ]
        }
        with open(llm_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")

        # Provenance Hash
        with open(local_image_path, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()
        with open(os.path.join(LEDGER_DIR, "ash_archive_cards.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"card": card["name"], "sha256": sha256, "model": ACTIVE_MODEL, "time": time.time()}) + "\n")
        safe_log(f"    [✓] Provenance Committed (SHA-256: {sha256[:12]}...)")
    except Exception as e:
        safe_log(f"    [!] Staging warning: {e}")

if __name__ == "__main__":
    safe_log(f"\n[*] Starting Batch Generation across 3 Major Gates...")
    for i, card in enumerate(CARDS, 1):
        safe_log(f"\n[{i}/3] Dispatching {card['name']} to ComfyUI ({ACTIVE_MODEL})...")
        payload = build_workflow(card)
        resp = queue_prompt(payload)
        if not resp:
            safe_log(f"[X] Submission rejected by server. Skipping {card['name']}.")
            continue
        prompt_id = resp['prompt_id']
        safe_log(f"    Queued as Prompt ID: {prompt_id}. Awaiting GPU execution...")

        while True:
            history = get_history(prompt_id)
            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                for node_id, node_output in outputs.items():
                    if "images" in node_output:
                        for img in node_output["images"]:
                            fn = img["filename"]
                            target = os.path.join(OUTPUT_DIR, fn)
                            download_image(fn, img.get("subfolder", ""), img.get("type", "output"), target)
                            safe_log(f"    [✓] Render Complete: {target}")
                            stage_card(card, target)
                break
            time.sleep(2.0)

    safe_log("\n============================================================")
    safe_log(f" [✓] Batch Complete! Forged cards saved in: {OUTPUT_DIR}/")
    safe_log("============================================================")
