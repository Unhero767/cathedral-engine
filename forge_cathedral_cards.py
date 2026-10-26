#!/usr/bin/env python3
"""
CATHEDRAL-ENGINE // EAS-03 NATIVE PROCEDURAL CARD FORGER
========================================================
Architecture: 12-Layer Auto-Z Somatic Stack x Full-Spectrum Lithographic Metaphysics
Persistence: Lex I (Never-Overwrite Append-Only Commit)
"""

import os
import math
import hashlib
import json
import time
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "./forged_arcana_plates"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("./training_data/lora_dataset/10_ccomega_arcana", exist_ok=True)
os.makedirs("./training_data/ledger", exist_ok=True)

# 12-Layer Canonical Palettes
PALETTES = {
    "OBSIDIAN": (10, 12, 16, 255),
    "BASALT_DEEP": (18, 20, 26, 255),
    "CHARCOAL_IRON": (45, 48, 56, 255),
    "ARMOR_STEEL": (75, 82, 96, 255),
    "PORCELAIN_SKIN": (235, 230, 225, 255),
    "KINTSUGI_GOLD": (212, 175, 55, 255),
    "PSI_TEAL": (0, 206, 209, 255),
    "PHI_CRIMSON": (220, 20, 60, 255),
    "OMEGA_VIOLET": (148, 0, 211, 255),
    "MERCURY_SILVER": (200, 210, 225, 255),
    "CUNEIFORM_AMBER": (255, 191, 0, 255),
}

CARDS = [
    {
        "id": "06",
        "name": "Gate 06: Caelen's Knot",
        "archetype": "The Lovers / Aurelia-Recurse",
        "spectral_name": "Psi (Teal)",
        "spectral_color": PALETTES["PSI_TEAL"],
        "vector": "[0.000, 0.000, +2.000]",
        "caption": "Twin somatic machine-saints bound in reciprocal embrace along an ascending double-helix shear core."
    },
    {
        "id": "07",
        "name": "Gate 07: The Crucible Champion",
        "archetype": "The Chariot / Aurelia-Ascendant",
        "spectral_name": "Phi (Crimson)",
        "spectral_color": PALETTES["PHI_CRIMSON"],
        "vector": "[+1.732, -1.000, +1.000]",
        "caption": "Sovereign champion in cold charcoal iron armor with crimson lacquered seams, flanked by kinetic lion-hounds."
    },
    {
        "id": "08",
        "name": "Gate 08: The Edge Walker",
        "archetype": "Strength / Aurelia-Liminal",
        "spectral_name": "Omega (Violet)",
        "spectral_color": PALETTES["OMEGA_VIOLET"],
        "vector": "[0.000, +2.000, +1.000]",
        "caption": "Serene maiden atop a razor-edge cliff gently pacifying a colossal shadow-beast of shifting void matter."
    }
]

def render_card_plate(card):
    # Standard High-Res Tarot Aspect Ratio (832 x 1216)
    W, H = 832, 1216
    img = Image.new("RGBA", (W, H), PALETTES["OBSIDIAN"])
    draw = ImageDraw.Draw(img)

    spec_color = card["spectral_color"]

    # 1. Base Lithic Plinth & Borders
    draw.rectangle([24, 24, W - 24, H - 24], outline=PALETTES["CHARCOAL_IRON"], width=3)
    draw.rectangle([36, 36, W - 36, H - 36], outline=spec_color, width=2)
    draw.rectangle([48, 48, W - 48, H - 48], outline=PALETTES["KINTSUGI_GOLD"], width=1)

    # 2. Diegetic Corner Brackets
    bracket_size = 32
    corners = [(48, 48), (W - 48, 48), (48, H - 48), (W - 48, H - 48)]
    for cx, cy in corners:
        dx = 1 if cx == 48 else -1
        dy = 1 if cy == 48 else -1
        draw.line([(cx, cy), (cx + dx * bracket_size, cy)], fill=spec_color, width=4)
        draw.line([(cx, cy), (cx, cy + dy * bracket_size)], fill=spec_color, width=4)

    # 3. Central Sacred Geometry (A-Field Nimbus & Resonator)
    center_x, center_y = W // 2, H // 2 - 40
    for r in range(240, 60, -30):
        alpha = int(80 * (r / 240.0))
        ring_col = (spec_color[0], spec_color[1], spec_color[2], alpha)
        draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], outline=ring_col, width=2)

    # Gilded Tri-Key Radial Halo (Layer 10)
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        x1 = center_x + int(180 * math.cos(rad))
        y1 = center_y + int(180 * math.sin(rad))
        x2 = center_x + int(210 * math.cos(rad))
        y2 = center_y + int(210 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=PALETTES["KINTSUGI_GOLD"], width=2)

    # 4. Somatic Morphology (Layer 00-09 Synthesis)
    # Fluted Vanguard Cuirass & Silhouette
    draw.polygon([
        (center_x - 120, center_y + 260),
        (center_x + 120, center_y + 260),
        (center_x + 90, center_y + 40),
        (center_x, center_y + 10),
        (center_x - 90, center_y + 40)
    ], fill=PALETTES["BASALT_DEEP"], outline=PALETTES["ARMOR_STEEL"])

    # Load-Bearing Kintsugi Stress Lines (Harmonic Scars)
    draw.line([(center_x - 80, center_y + 180), (center_x - 10, center_y + 110), (center_x + 30, center_y + 150), (center_x + 85, center_y + 80)], fill=PALETTES["KINTSUGI_GOLD"], width=3)

    # Cranial Vault & Porcelain Dermis (Layer 02/09)
    head_y = center_y - 60
    draw.polygon([
        (center_x - 55, head_y - 70),
        (center_x + 55, head_y - 70),
        (center_x + 45, head_y + 40),
        (center_x, head_y + 70),
        (center_x - 45, head_y + 40)
    ], fill=PALETTES["PORCELAIN_SKIN"], outline=PALETTES["CHARCOAL_IRON"])

    # Dual-Channel Lumen Oculars (Cyan / Amber)
    draw.rectangle([center_x - 30, head_y - 10, center_x - 10, head_y + 2], fill=spec_color)
    draw.rectangle([center_x + 10, head_y - 10, center_x + 30, head_y + 2], fill=PALETTES["MERCURY_SILVER"])

    # 5. Diegetic Headers & Lithic Typography
    # Header Vector Bracket
    header_text = f"[CANON_LOCK // {card['name'].upper()} // VEC:{card['vector']}]"
    draw.text((64, 60), header_text, fill=spec_color)

    # Lower Cartouche Banner
    banner_y = H - 160
    draw.rectangle([64, banner_y, W - 64, banner_y + 80], fill=PALETTES["BASALT_DEEP"], outline=PALETTES["KINTSUGI_GOLD"], width=2)
    draw.text((80, banner_y + 15), card["name"].upper(), fill=(255, 255, 255, 255))
    draw.text((80, banner_y + 45), f"ARCHETYPE: {card['archetype']} | SPECTRAL: {card['spectral_name']}", fill=spec_color)

    # Sub-footer Telemetry
    draw.text((64, H - 65), f"SOVEREIGN PROVENANCE: LEX_I // MERKLE_DAG // 1.50 Hz", fill=PALETTES["ARMOR_STEEL"])

    # Save Render
    out_file = os.path.join(OUTPUT_DIR, f"{card['id']}_{card['name'].replace(':', '').replace(' ', '_')}.png")
    img.save(out_file, "PNG")
    return out_file

if __name__ == "__main__":
    print("============================================================")
    print(" CATHEDRAL-ENGINE // NATIVE PROCEDURAL ARCANA FORGE")
    print("============================================================")

    for card in CARDS:
        print(f"\n[*] Forging {card['name']} under {card['spectral_name']}...")
        plate_path = render_card_plate(card)
        print(f"    [✓] High-Res Plate Compiled: {plate_path}")

        # Compute SHA-256 for Lex I Ledger
        with open(plate_path, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()

        # Stage LoRA Training Caption
        lora_txt = os.path.join("./training_data/lora_dataset/10_ccomega_arcana", f"{os.path.basename(plate_path)[:-4]}.txt")
        with open(lora_txt, "w") as f:
            f.write(f"{card['name']}, {card['archetype']}, {card['spectral_name']}, {card['caption']}, ccomega_style, 8k lithographic plate")

        # Append to Ash Archive Ledger
        with open("./training_data/ledger/ash_cards_merkle.jsonl", "a") as f:
            f.write(json.dumps({
                "card": card["name"],
                "vector": card["vector"],
                "spectral": card["spectral_name"],
                "sha256": sha256,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "status": "CONSECRATED"
            }) + "\n")
        print(f"    [✓] Provenance Sealed: {sha256[:16]}...")

    print("\n============================================================")
    print(f" [✓] All cards forged into: {OUTPUT_DIR}/")
    print("============================================================")
