import os, re

# Known type mappings for Cathedral-Engine scripts
type_mappings = {
    'glitch_wastes': 'extends Node2D',
    'player_soulframe': 'extends CharacterBody2D',
    'carrier_synthesizer': 'extends Node',
    'chamber_v': 'extends Node2D',
    'chamberv': 'extends Node2D',
    'cathedral_sync': 'extends Node',
    'resonance_screen': 'extends CanvasItem'
}

patched = 0
for root, _, files in os.walk('.'):
    for f in files:
        if f.endswith('.gd'):
            f_path = os.path.join(root, f)
            with open(f_path, 'r', encoding='utf-8', errors='ignore') as gf:
                content = gf.read()
            
            lines = [l.strip() for l in content.splitlines()]
            has_add_child = any('add_child(' in l for l in lines)
            has_extends = any(l.startswith('extends') for l in lines)
            
            if has_add_child and not has_extends:
                base_name = f.replace('.gd', '').lower()
                chosen_ext = type_mappings.get(base_name, 'extends Node')
                
                new_content = f"{chosen_ext}\n\n" + content
                with open(f_path, 'w', encoding='utf-8') as gf:
                    gf.write(new_content)
                
                print(f"[✓] Added '{chosen_ext}' to: {f_path}")
                patched += 1

print(f"\n[✓] Audit complete. Patched {patched} script(s).")
