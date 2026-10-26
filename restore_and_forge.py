#!/usr/bin/env python3
import json
import os
import glob
import time
import urllib.request
import urllib.parse
import urllib.error
import uuid
import sys
from PIL import Image

SERVER_ADDRESS = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())

GATE_06_PROMPT = (
    "(masterpiece, best quality:1.3), (gate_06_caelens_knot:1.3), (the_lovers_aurelia_recurse:1.2), "
    "6-star gacha card splash art, tarot card composition, CC-Omega lithographic visual doctrine, Regime 03 Spectral, "
    "twin somatic machine-saint figures intertwined in reciprocal embrace around an ascending double-helix basalt pillar, "
    "porcelain synth-skin, heterochromatic cyan aperture-ring eyes, braided split silver and obsidian hair, "
    "asymmetrical gunmetal armor plates, glowing matte teal spectrafilaments, gold kintsugi stress fractures, "
    "liquid mercury pooling at feet, upward volumetric light shafts, colored chiaroscuro with teal key bias, "
    "sacred geometric cuneiform halo, 8k resolution, razor-sharp focus"
)

def find_reference_png():
    """Locates an existing successful living_arcana render."""
    search_paths = [
        ".",
        "./output",
        os.path.expanduser("~/ComfyUI/output"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/cathedral_engine"),
        os.path.expanduser("~/cathedral_engine/forged_arcana_plates"),
    ]
    for p in search_paths:
        matches = glob.glob(os.path.join(p, "*living_arcana*card*.png")) + glob.glob(os.path.join(p, "*living_arcana*.png"))
        if matches:
            # Sort newest first
            matches.sort(key=os.path.getmtime, reverse=True)
            return matches[0]
    return None

ref_path = find_reference_png()
if not ref_path:
    print("[!] Could not auto-locate a previous living_arcana*.png.")
    print("    Please provide the path to living_arcana_card_01_00001_.png:")
    try:
        user_input = input("Path: ").strip()
        if os.path.exists(user_input):
            ref_path = user_input
        else:
            sys.exit(1)
    except (EOFError, KeyboardInterrupt):
        sys.exit(1)

print(f"\n[*] Found reference card: {ref_path}")

# Extract embedded ComfyUI metadata from PNG
try:
    img = Image.open(ref_path)
    info = img.info
except Exception as e:
    print(f"[!] Error opening image: {e}")
    sys.exit(1)

if "prompt" not in info:
    print("[!] No embedded ComfyUI prompt metadata found in this PNG.")
    sys.exit(1)

prompt_graph = json.loads(info["prompt"])

# Save UI workflow JSON for drag-and-drop into browser
if "workflow" in info:
    ui_workflow = json.loads(info["workflow"])
    with open("restored_living_arcana_ui.json", "w", encoding="utf-8") as f:
        json.dump(ui_workflow, f, indent=2)
    print("[✓] Exported: restored_living_arcana_ui.json (you can drag this onto your ComfyUI canvas!)")

# Identify nodes to update
pos_node_id = None
save_node_id = None
ksampler_id = None

for node_id, node in prompt_graph.items():
    ctype = node.get("class_type", "")
    inputs = node.get("inputs", {})
    
    if ctype == "KSampler":
        ksampler_id = node_id
    elif ctype == "SaveImage":
        save_node_id = node_id

# Find positive prompt node connected to KSampler
if ksampler_id and "positive" in prompt_graph[ksampler_id].get("inputs", {}):
    pos_link = prompt_graph[ksampler_id]["inputs"]["positive"]
    if isinstance(pos_link, list) and len(pos_link) > 0:
        pos_node_id = str(pos_link[0])

# Fallback: scan for CLIPTextEncode
if not pos_node_id:
    for node_id, node in prompt_graph.items():
        if node.get("class_type") == "CLIPTextEncode":
            text = node.get("inputs", {}).get("text", "")
            if not any(k in text.lower() for k in ["low quality", "bad anatomy", "worst quality"]):
                pos_node_id = node_id
                break

if not pos_node_id:
    print("[!] Could not locate positive prompt node in extracted graph.")
    sys.exit(1)

print(f"[*] Updating Positive Prompt Node [{pos_node_id}] with Gate 06...")
prompt_graph[pos_node_id]["inputs"]["text"] = GATE_06_PROMPT

if save_node_id:
    prompt_graph[save_node_id]["inputs"]["filename_prefix"] = "living_arcana_card_06"
    print(f"[*] Updated SaveImage prefix to: 'living_arcana_card_06'")

if ksampler_id and "seed" in prompt_graph[ksampler_id].get("inputs", {}):
    prompt_graph[ksampler_id]["inputs"]["seed"] = 44189426

# Submit to ComfyUI
def queue_prompt(prompt_dict):
    p = {"prompt": prompt_dict, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"\n[!] ComfyUI Rejection: {e.read().decode('utf-8')}")
        sys.exit(1)

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as resp:
        return json.loads(resp.read().decode('utf-8'))

def download_image(filename, subfolder, folder_type, output_path):
    params = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": folder_type})
    url = f"http://{SERVER_ADDRESS}/view?{params}"
    urllib.request.urlretrieve(url, output_path)

print(f"\n[*] Dispatching Gate 06 to ComfyUI using your verified workflow...")
queued = queue_prompt(prompt_graph)
prompt_id = queued['prompt_id']
print(f"[+] Task Queued (Prompt ID: {prompt_id}). Generating...")

while True:
    history = get_history(prompt_id)
    if prompt_id in history:
        outputs = history[prompt_id].get("outputs", {})
        for node_id, node_output in outputs.items():
            if "images" in node_output:
                for img_meta in node_output["images"]:
                    fn = img_meta["filename"]
                    target = f"./{fn}"
                    download_image(fn, img_meta.get("subfolder", ""), img_meta.get("type", "output"), target)
                    print(f"\n[✓] Forged card completed and saved: {target}")
        break
    time.sleep(2.0)
