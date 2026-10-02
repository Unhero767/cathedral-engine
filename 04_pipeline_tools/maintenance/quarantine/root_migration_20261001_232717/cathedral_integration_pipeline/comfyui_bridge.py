"""
Module 1: ComfyUI REST & WebSocket Automation Bridge
Provides headless batch generation of 4096x128 atlas strips from Character Recipe JSONs.
"""
import urllib.request
import urllib.parse
import json
import os
import time
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transducer import BioSemanticTransducer
from atlas_compiler import AtlasCompiler

class ComfyUIBridge:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.transducer = BioSemanticTransducer()
        self.compiler = AtlasCompiler()

    def check_server_status(self) -> bool:
        try:
            url = f"http://{self.server_address}/system_stats"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                return resp.status == 200
        except Exception:
            return False

    def build_workflow_payload(self, recipe_data: dict) -> dict:
        trans_res = self.transducer.transduce(recipe_data)
        slug = recipe_data.get("archetype", "custom").lower().replace(" ", "_").replace("-", "_")
        
        workflow_graph = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": 6.5,
                    "denoise": 1.0,
                    "latent_image": ["5", 0],
                    "model": ["4", 0],
                    "negative": ["7", 0],
                    "positive": ["6", 0],
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "seed": 76701,
                    "steps": 30
                }
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {"batch_size": 1, "height": 512, "width": 512}
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["4", 1], "text": trans_res["comfyui_prompts"]["positive"]}
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": ["4", 1], "text": trans_res["comfyui_prompts"]["negative"]}
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]}
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {"filename_prefix": f"MLAOS_Atlas_{slug}", "images": ["8", 0]}
            }
        }
        return {"prompt": workflow_graph, "client_id": "CathedralEngine_Headless"}

    def generate_atlas_headlessly(self, recipe_path: str, output_tres_dir: str) -> dict:
        with open(recipe_path, "r", encoding="utf-8") as f:
            recipe_data = json.load(f)
        
        archetype = recipe_data.get("archetype", "Unknown")
        slug = archetype.lower().replace(" ", "_").replace("-", "_")
        tres_out = os.path.join(output_tres_dir, f"{slug}_spriteframes.tres")
        
        is_live = self.check_server_status()
        if is_live:
            payload = self.build_workflow_payload(recipe_data)
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data_bytes, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
            prompt_id = resp_json.get("prompt_id", "queued")
            status_msg = f"Queued in ComfyUI API (Prompt ID: {prompt_id})"
        else:
            status_msg = "ComfyUI offline; compiled .tres from local template bridge."

        self.compiler.generate_godot4_spriteframes_tres(f"res://cathedral_integration_pipeline/assets/{slug}_atlas.png", tres_out)
        
        return {
            "archetype": archetype,
            "status": status_msg,
            "tres_path": tres_out,
            "comfyui_online": is_live
        }
