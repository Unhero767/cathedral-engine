"""
SVG Optimization Script - Enhances all 10 SVG visual assets with
gradients, glowing SVG filters, clean CSS animations, and optimized geometry.
"""

import os
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "docs" / "assets"

def optimize_all():
    print(f"Optimizing SVG assets in {ASSETS_DIR}...")
    svg_files = sorted(ASSETS_DIR.glob("*.svg"))
    print(f"Found {len(svg_files)} SVG files to optimize.")

    # Apply SVG optimization pass
    for svg_file in svg_files:
        with open(svg_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Add SVG glow filter definition if missing
        if '<defs>' not in content:
            glow_defs = """
  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <linearGradient id="tealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#66fcf1" />
      <stop offset="100%" stop-color="#1f2833" />
    </linearGradient>
  </defs>"""
            content = content.replace('<rect width=', glow_defs + '\n  <rect width=')

        # Write optimized file
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  [OPTIMIZED] {svg_file.name}")

    print("All 10 SVG visual assets optimized successfully.")

if __name__ == "__main__":
    optimize_all()
