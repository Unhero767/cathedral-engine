#!/usr/bin/env python3
"""
Cathedral-Engine ComfyUI LoRA Integration Script
Verifies and links the compiled Anima MLAOS LoRA weights into ComfyUI.
"""

import os
from pathlib import Path

WORKSPACE_DIR = Path("/Users/kennethdallmier/cathedral_engine")
OUTPUT_LORA = WORKSPACE_DIR / "output" / "anima_mlaops_lora" / "anima_mlaops_lora_final.safetensors"
COMFY_LORA_DIR = WORKSPACE_DIR.parent / "ComfyUI" / "models" / "loras"

def link_lora_to_comfy():
    print(f"[MLAOS-ARBITER] Verifying compiled LoRA artifact at: {OUTPUT_LORA}")
    if not OUTPUT_LORA.exists():
        print(f"[ERROR] LoRA weights not found at {OUTPUT_LORA}. Run training script first.")
        return

    print(f"[MLAOS-ARBITER] Checking ComfyUI loras directory: {COMFY_LORA_DIR}")
    COMFY_LORA_DIR.mkdir(parents=True, exist_ok=True)
    
    target_symlink = COMFY_LORA_DIR / "anima_mlaops_lora_final.safetensors"
    
    if target_symlink.exists() or target_symlink.is_symlink():
        target_symlink.unlink()
        
    target_symlink.symlink_to(OUTPUT_LORA)
    print(f"[SUCCESS] LoRA successfully linked for ComfyUI inference: {target_symlink}")
    print(f"[EXECUTION READY] Add a 'Load LoRA' node in your ComfyUI workflow and select 'anima_mlaops_lora_final.safetensors'.")

if __name__ == "__main__":
    link_lora_to_comfy()
