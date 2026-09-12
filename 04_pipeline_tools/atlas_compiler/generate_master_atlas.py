#!/usr/bin/env python3
"""
Zero-dependency 4096x128 Master Atlas PNG Generator for EAS-03 Avatar Engine.
Uses only Python built-in standard library (zlib, struct, math).
"""

import math
import struct
import zlib

def write_png(filename, width, height, rgba_data):
    def make_chunk(chunk_type, data):
        length = struct.pack(">I", len(data))
        crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xffffffff)
        return length + chunk_type + data + crc

    # PNG Signature
    png = b"\x89PNG\r\n\x1a\n"
    
    # IHDR Chunk (width, height, 8-bit depth, RGBA color type 6)
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png += make_chunk(b"IHDR", ihdr_data)
    
    # Raw scanlines with filter byte 0 (None)
    raw_lines = bytearray()
    for y in range(height):
        raw_lines.append(0) # Filter byte
        start = y * width * 4
        end = start + width * 4
        raw_lines.extend(rgba_data[start:end])
        
    compressed_idat = zlib.compress(bytes(raw_lines), 6)
    png += make_chunk(b"IDAT", compressed_idat)
    png += make_chunk(b"IEND", b"")
    
    with open(filename, "wb") as f:
        f.write(png)

WIDTH = 4096
HEIGHT = 128
FRAME_SIZE = 128
NUM_FRAMES = 32

buf = bytearray(WIDTH * HEIGHT * 4)

def set_pixel(x, y, r, g, b, a=255):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        idx = (y * WIDTH + x) * 4
        buf[idx] = r
        buf[idx + 1] = g
        buf[idx + 2] = b
        buf[idx + 3] = a

def draw_rect(x1, y1, x2, y2, r, g, b, a=255):
    for y in range(max(0, y1), min(HEIGHT, y2)):
        for x in range(max(0, x1), min(WIDTH, x2)):
            set_pixel(x, y, r, g, b, a)

def draw_circle_outline(cx, cy, radius, r, g, b, thickness=3):
    r_inner_sq = (radius - thickness) ** 2
    r_outer_sq = radius ** 2
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            d_sq = (x - cx) ** 2 + (y - cy) ** 2
            if r_inner_sq <= d_sq <= r_outer_sq:
                set_pixel(x, y, r, g, b)

# 12-Layer Palette
ARMOR_STEEL = (75, 82, 96)
ARMOR_HIGHLIGHT = (140, 150, 170)
GOLD_HALO = (255, 210, 72)
CYAN_EYE = (0, 235, 255)
SKIN_PORCELAIN = (225, 220, 215)
ROBE_INDIGO = (32, 40, 65)

for f in range(NUM_FRAMES):
    offset_x = f * FRAME_SIZE
    cx = offset_x + 64
    cy = 64
    
    if f < 4: # liturgical_idle (0..3)
        breathe = math.sin(f / 4.0 * math.pi * 2) * 1.5
        halo_glow = 1.0
        eye_glow = 1.0
        jaw_open = 0
        shift = 0
    elif f < 10: # lumen_pulse (4..9)
        phase = (f - 4) / 6.0
        breathe = math.sin(phase * math.pi * 2) * 3.0
        halo_glow = 1.0 + math.sin(phase * math.pi * 2) * 0.4
        eye_glow = 1.0
        jaw_open = 0
        shift = 0
    elif f < 16: # ocular_surge (10..15)
        phase = (f - 10) / 6.0
        breathe = 0.0
        halo_glow = 1.0
        eye_glow = 1.5 + math.sin(phase * math.pi * 2) * 0.5
        jaw_open = 0
        shift = 0
    elif f < 24: # harmonic_resonance (16..23)
        phase = (f - 16) / 8.0
        breathe = math.sin(phase * math.pi * 2) * 2.0
        halo_glow = 1.6 + math.cos(phase * math.pi * 2) * 0.6
        eye_glow = 1.3
        jaw_open = 0
        shift = 0
    elif f < 28: # dialetheic_shift (24..27)
        phase = (f - 24) / 4.0
        breathe = 0.0
        halo_glow = 1.2
        eye_glow = 1.4
        jaw_open = 0
        shift = int(math.sin(phase * math.pi * 2) * 3)
    else: # penitent_recitation (28..31)
        phase = (f - 28) / 4.0
        breathe = 1.0
        halo_glow = 1.1
        eye_glow = 1.2
        jaw_open = int(abs(math.sin(phase * math.pi * 2)) * 4)
        shift = 0
        
    head_cy = int(cy - 12 + breathe)
    
    # 1. Gilded Tri-Key Halo (Layer 10 - Theta Gold Constant)
    hr = int(36 * (0.95 + halo_glow * 0.05))
    hg = (
        min(255, int(GOLD_HALO[0] * min(1.3, halo_glow))),
        min(255, int(GOLD_HALO[1] * min(1.3, halo_glow))),
        min(255, int(GOLD_HALO[2] * min(1.3, halo_glow)))
    )
    draw_circle_outline(cx, head_cy, hr, hg[0], hg[1], hg[2], thickness=3)
    
    # 2. Monastic Shroud (Layer 04/07)
    draw_rect(cx - 30, head_cy + 10, cx + 30, cy + 52, ROBE_INDIGO[0], ROBE_INDIGO[1], ROBE_INDIGO[2])
    
    # 3. Fluted Cuirass Plate (Layer 05)
    draw_rect(cx - 18, head_cy + 16, cx + 18, cy + 48, ARMOR_STEEL[0], ARMOR_STEEL[1], ARMOR_STEEL[2])
    draw_rect(cx - 1, head_cy + 16, cx + 1, cy + 48, ARMOR_HIGHLIGHT[0], ARMOR_HIGHLIGHT[1], ARMOR_HIGHLIGHT[2])
    
    # 4. Cranial Armature (Layer 00/02)
    draw_rect(cx - 14 + shift, head_cy - 18, cx + 14 + shift, head_cy + 12 + jaw_open, SKIN_PORCELAIN[0], SKIN_PORCELAIN[1], SKIN_PORCELAIN[2])
    
    # 5. Ocular Lenses (Layer 09 - Psi Cyan Constant)
    ec = (
        0,
        min(255, int(CYAN_EYE[1] * min(1.2, eye_glow))),
        min(255, int(CYAN_EYE[2] * min(1.2, eye_glow)))
    )
    draw_rect(cx - 8 + shift, head_cy - 4, cx - 3 + shift, head_cy, ec[0], ec[1], ec[2])
    draw_rect(cx + 3 + shift, head_cy - 4, cx + 8 + shift, head_cy, ec[0], ec[1], ec[2])

write_png('aurelia9_atlas_strip.png', WIDTH, HEIGHT, buf)
print("Successfully generated aurelia9_atlas_strip.png (4096x128 RGBA).")
