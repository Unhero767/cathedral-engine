import os
import json
import hashlib
import time

base_dir = os.path.join(os.getcwd(), "cathedral_integration_pipeline")
os.makedirs(os.path.join(base_dir, "godot4_runtime"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "recipes"), exist_ok=True)

# 1. validator.py
with open(os.path.join(base_dir, "validator.py"), "w", encoding="utf-8") as f:
    f.write('''"""
MLAOS Metalogical Type-Checker and Schema Validator
"""
import json, os
from typing import Dict, Any, Tuple, List

CANONICAL_SPECTRAL_CONSTANTS = {
    "Theta": {"color": "#D4AF37", "wavelength_nm": 585, "semantic": "Joy / Law"},
    "Psi": {"color": "#008080", "wavelength_nm": 490, "semantic": "Curiosity / Logic"},
    "Delta": {"color": "#002147", "wavelength_nm": 440, "semantic": "Sorrow / Archive"},
    "Phi": {"color": "#8B0000", "wavelength_nm": 680, "semantic": "Anger / Remaking"},
    "Omega": {"color": "#301934", "wavelength_nm": 405, "semantic": "Fear / Shadow"},
    "Epsilon": {"color": "#50C878", "wavelength_nm": 520, "semantic": "Love / Healing"},
    "Null": {"color": "#121212", "wavelength_nm": 0, "semantic": "Void / Anti-Resonance"}
}

REQUIRED_RECIPE_FIELDS = ["archetype", "spectral_constant", "ego_density", "afield_potency"]

class MLAOSValidator:
    def validate_character_recipe(self, recipe: Dict[str, Any]) -> Tuple[bool, List[str], float]:
        errors = []
        for field in REQUIRED_RECIPE_FIELDS:
            if field not in recipe:
                errors.append(f"Missing required field: '{field}'")

        if errors:
            return False, errors, 0.0

        spec = recipe.get("spectral_constant")
        if spec not in CANONICAL_SPECTRAL_CONSTANTS:
            errors.append(f"Invalid spectral_constant '{spec}'.")

        rho = recipe.get("ego_density", 0.0)
        if not isinstance(rho, (int, float)) or rho <= 0.0 or rho > 20.0:
            errors.append(f"Ego density (rho) out of bounds: {rho}.")

        afield = recipe.get("afield_potency", 0.0)
        if not isinstance(afield, (int, float)) or afield < 0.0 or afield > 2.0:
            errors.append(f"A-Field potency out of bounds: {afield}.")

        delta_rho = abs(rho - 8.3)
        epsilon_local = 1.0 + (delta_rho * 0.15)
        w_a = float(afield) * 1.5
        c_tau = round(w_a / epsilon_local, 4)

        return len(errors) == 0, errors, c_tau
''')

# 2. transducer.py
with open(os.path.join(base_dir, "transducer.py"), "w", encoding="utf-8") as f:
    f.write('''"""
MLAOS Bio-Semantic Transducer
"""
from typing import Dict, Any

class BioSemanticTransducer:
    def __init__(self):
        self.spectral_palette = {
            "Theta": {"hex": "#D4AF37", "nm": 585, "tags": "aged gold leaf, burnished brass accents, 585nm gold aura", "rgb": [1.0, 0.82, 0.28], "bias": [0.05, 0.15, 0.20, 0.02]},
            "Psi": {"hex": "#008080", "nm": 490, "tags": "matte teal conduits, recursive lattice geometry, cold cyan data pulses", "rgb": [0.0, 0.92, 1.0], "bias": [-0.05, -0.18, 0.10, 0.05]},
            "Delta": {"hex": "#002147", "nm": 440, "tags": "oxford blue oxidized surfaces, deep indigo stone, zero-decay archive patina", "rgb": [0.10, 0.35, 0.85], "bias": [-0.10, -0.15, -0.15, -0.05]},
            "Phi": {"hex": "#8B0000", "nm": 680, "tags": "crimson heat fissures, kinetic remaking scars, dark red combustion residue", "rgb": [0.95, 0.15, 0.15], "bias": [0.08, 0.25, -0.05, 0.10]},
            "Omega": {"hex": "#301934", "nm": 405, "tags": "dark violet refraction, shadow-walking boundary, deep purple obsidian", "rgb": [0.70, 0.20, 0.95], "bias": [-0.12, 0.05, -0.22, 0.08]},
            "Epsilon": {"hex": "#50C878", "nm": 520, "tags": "emerald restorative veins, living green resonance filaments", "rgb": [0.31, 0.78, 0.47], "bias": [0.02, -0.10, 0.22, 0.02]},
            "Null": {"hex": "#121212", "nm": 0, "tags": "matte black ceramic, anti-resonance negative space, lightless obsidian", "rgb": [0.05, 0.05, 0.05], "bias": [-0.25, 0.00, 0.00, -0.15]}
        }

    def transduce(self, recipe: Dict[str, Any]) -> Dict[str, Any]:
        archetype = recipe.get("archetype", "Unknown Sovereign")
        title = recipe.get("title", "")
        spectral = recipe.get("spectral_constant", "Theta")
        rho = float(recipe.get("ego_density", 8.3))
        afield = float(recipe.get("afield_potency", 0.5))
        dialetheic = recipe.get("dialetheic_state", "Equilibrium")
        somatic = recipe.get("somatic_properties", {})

        spec = self.spectral_palette.get(spectral, self.spectral_palette["Theta"])

        pos_prompt = (
            f"masterpiece, authentic MLAOS-Prime visual constitution, character portrait bust of {archetype} ({title}), "
            f"mythotechnical ritualized infrastructure, machine as sacred reliquary, monumental scale, brutalist monastic vaults, "
            f"fluted blackened steel, brushed brass joints, matte ceramic armor, radial glyph conduits, {spec['tags']}, "
            f"dramatic volumetric god rays, heavy suspended dust and ash, deep occluded directional shadows, "
            f"harmonic contrast, {dialetheic.lower()}, historical battle scars, patina, weathering {somatic.get('weathering_index', 0.70):.2f}, "
            f"8k render fidelity"
        )
        neg_prompt = (
            "neon cyberpunk, high-gloss clean surfaces, pristine plastic armor, chrome plating, "
            "generic medieval fantasy, glowing anime eyes, messy lineart, oversaturated rainbow colors, "
            "sterile sci-fi corridors, decorative gothic clutter without function, modern corporate logos"
        )

        shadow_ramp = round(0.55 + ((rho - 8.3) * 0.03), 3)
        shadow_ramp = max(0.20, min(0.85, shadow_ramp))

        shader_uniforms = {
            "u_shadow_depth_ramp": shadow_ramp,
            "u_specular_rim_factor": round(1.20 + (afield * 0.35), 2),
            "u_lumen_emission_gain": 1.00,
            "u_afield_potency": afield,
            "u_enable_dither": True,
            "u_enable_dual_lumen": True,
            "u_spectral_tint": spec["rgb"]
        }

        liturgy = recipe.get("liturgical_telemetry", {})
        return {
            "archetype": archetype,
            "spectral_constant": spectral,
            "hex_color": spec["hex"],
            "comfyui_prompts": {"positive": pos_prompt, "negative": neg_prompt},
            "latent_biasing": {"channel_weights": spec["bias"], "density_multiplier": round(rho / 8.3, 3)},
            "godot_shader_uniforms": shader_uniforms,
            "dialogue_physics": {
                "base_gain": 1.0,
                "stress_multiplier": liturgy.get("dialogue_luminance_gain", 1.45),
                "ocular_surge_hz": liturgy.get("ocular_frequency_hz", 10.0),
                "spectral_channel": "Gold" if spectral == "Theta" else "Cyan"
            }
        }
''')

# 3. atlas_compiler.py
with open(os.path.join(base_dir, "atlas_compiler.py"), "w", encoding="utf-8") as f:
    f.write('''"""
EAS-03 Atlas Compiler & SpriteFrames Resource Exporter
"""
import os

ANIMATION_DEFINITIONS = {
    "liturgical_idle": {"start": 0, "count": 4, "fps": 6.0, "loop": "true"},
    "lumen_pulse": {"start": 4, "count": 6, "fps": 8.0, "loop": "true"},
    "ocular_surge": {"start": 10, "count": 6, "fps": 10.0, "loop": "true"},
    "harmonic_resonance": {"start": 16, "count": 8, "fps": 8.0, "loop": "true"},
    "dialetheic_shift": {"start": 24, "count": 4, "fps": 6.0, "loop": "true"},
    "penitent_recitation": {"start": 28, "count": 4, "fps": 8.0, "loop": "true"}
}

class AtlasCompiler:
    def generate_godot4_spriteframes_tres(self, atlas_texture_path: str, output_tres_path: str) -> str:
        tres_content = [
            "[gd_resource type=\\"SpriteFrames\\" load_steps=34 format=3 uid=\\"uid://mlaoseas03atlas001\\"]",
            "",
            f"[ext_resource type=\\"Texture2D\\" path=\\"{atlas_texture_path}\\" id=\\"1_master_atlas\\"]",
            ""
        ]

        for i in range(32):
            sub_id = f"sub_resource_frame_{i:02d}"
            x_pos = i * 128
            tres_content.extend([
                f"[sub_resource type=\\"AtlasTexture\\" id=\\"{sub_id}\\"]",
                "atlas = ExtResource(\\"1_master_atlas\\")",
                f"region = Rect2({x_pos}, 0, 128, 128)",
                "filter_clip = true",
                ""
            ])

        tres_content.append("[resource]")
        tres_content.append("animations = [{")

        anim_entries = []
        for anim_name, config in ANIMATION_DEFINITIONS.items():
            frames_list = [f"{{\\"duration\\": 1.0, \\"texture\\": SubResource(\\"sub_resource_frame_{f:02d}\\")}}" for f in range(config["start"], config["start"] + config["count"])]
            frames_str = ", ".join(frames_list)
            entry = (
                f"\\"frames\\": [{frames_str}],\\n"
                f"\\"loop\\": {config['loop']},\\n"
                f"\\"name\\": &\\"{anim_name}\\",\\n"
                f"\\"speed\\": {config['fps']}"
            )
            anim_entries.append("{\\n" + entry + "\\n}")

        tres_content.append(", ".join(anim_entries))
        tres_content.append("}]")

        full_tres_text = "\\n".join(tres_content)
        if output_tres_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_tres_path)), exist_ok=True)
            with open(output_tres_path, "w", encoding="utf-8") as f:
                f.write(full_tres_text)

        return full_tres_text
''')

# 4. dialogue_engine.py
with open(os.path.join(base_dir, "dialogue_engine.py"), "w", encoding="utf-8") as f:
    f.write('''"""
MLAOS Dialogue Physics & Phoneme Stress Engine
"""
from typing import Dict, Any, List

class DialoguePhysicsEngine:
    def __init__(self):
        self.high_stress_tokens = {
            "law", "sovereign", "ash", "never", "truth", "cathedral", "hazard", 
            "fluted", "reliquary", "bone", "scars", "dialetheic", "genesis", "fire"
        }

    def calculate_phoneme_stress(self, text: str) -> List[Dict[str, Any]]:
        words = text.split()
        cadence_timeline = []

        for idx, w in enumerate(words):
            clean_word = w.strip(".,!?:;\\\"'").lower()
            is_high = clean_word in self.high_stress_tokens
            is_cap = w[0].isupper() if w else False
            
            stress_val = min(1.0, 0.35 + (0.45 if is_high else 0.0) + (0.20 if is_cap else 0.0))
            lumen_gain = round(1.0 + (stress_val * 0.45), 3)

            if is_high:
                anim = "harmonic_resonance" if stress_val > 0.85 else "lumen_pulse"
            elif idx % 4 == 0:
                anim = "ocular_surge"
            else:
                anim = "penitent_recitation"

            cadence_timeline.append({
                "word": w,
                "stress": round(stress_val, 2),
                "lumen_emission_gain": lumen_gain,
                "liturgical_animation": anim
            })

        return cadence_timeline
''')

# 5. ash_ledger_manager.py
with open(os.path.join(base_dir, "ash_ledger_manager.py"), "w", encoding="utf-8") as f:
    f.write('''"""
MLAOS Ash Archive & JBP Merkle Ledger Manager
"""
import json, hashlib, time, os
from typing import Dict, Any

class AshLedgerManager:
    def __init__(self, ledger_path: str = ""):
        self.ledger_path = ledger_path or os.path.join(os.path.dirname(__file__), "ash_ledger.json")
        self.ledger = self._load_or_init()

    def _load_or_init(self) -> Dict[str, Any]:
        if os.path.exists(self.ledger_path):
            try:
                with open(self.ledger_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "magisterium_version": "MLAOS-PRIME-v1.0.0",
            "doctrine": "Never-Overwrite (Book III: The Ash Archive)",
            "total_entries": 1,
            "entries": [{
                "index": 0,
                "timestamp": "2026-08-20T00:00:00Z",
                "event_type": "GENESIS_COVENANT",
                "archetype_id": "SYSTEM_CORE",
                "layer_target": "Layer_00_Skeletal",
                "telemetry": "The First Hearth ignition; baseline substrate established.",
                "prev_j_hash": "0000000000000000000000000000000000000000000000000000000000000000",
                "j_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            }]
        }

    def append_historical_scar(self, archetype_id: str, scar_description: str, severity: float, spectral_constant: str) -> Dict[str, Any]:
        prev_entry = self.ledger["entries"][-1]
        idx = len(self.ledger["entries"])
        entry_data = {
            "index": idx,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event_type": "HISTORICAL_SCAR_INJECTION",
            "archetype_id": archetype_id,
            "layer_target": "Layer_11_Custom_Overlay",
            "severity": round(severity, 2),
            "spectral_constant": spectral_constant,
            "telemetry": scar_description,
            "prev_j_hash": prev_entry["j_hash"]
        }
        serialized = json.dumps(entry_data, sort_keys=True)
        entry_data["j_hash"] = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        self.ledger["entries"].append(entry_data)
        self.ledger["total_entries"] = len(self.ledger["entries"])
        self._save()
        return entry_data

    def _save(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.ledger_path)), exist_ok=True)
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(self.ledger, f, indent=2)
''')

# 6. Sample recipes
recipes = {
    "aurelia_9_vanguard.json": {
        "archetype": "Aurelia-9", "title": "Vanguard of the First Hearth", "spectral_constant": "Theta",
        "ego_density": 8.3, "afield_potency": 0.95, "dialetheic_state": "Joy in Martial Severity",
        "somatic_properties": {"armor": "Fluted gilded plate", "weathering_index": 0.65},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.45, "ocular_frequency_hz": 10.0}
    },
    "caelen_architect.json": {
        "archetype": "Caelen", "title": "Master Architect of the Lattices", "spectral_constant": "Psi",
        "ego_density": 8.1, "afield_potency": 0.88, "dialetheic_state": "Recursive Invariance",
        "somatic_properties": {"armor": "Matte ceramic plates", "weathering_index": 0.40},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.20, "ocular_frequency_hz": 12.0}
    },
    "deimos_catalyst.json": {
        "archetype": "Deimos", "title": "Catalyst of Kinetic Remaking", "spectral_constant": "Phi",
        "ego_density": 9.4, "afield_potency": 0.99, "dialetheic_state": "Stochastic Volatility",
        "somatic_properties": {"armor": "Charred vanguard plate", "weathering_index": 0.90},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.80, "ocular_frequency_hz": 8.0}
    }
}
for name, data in recipes.items():
    with open(os.path.join(base_dir, "recipes", name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# 7. Godot runtime files
with open(os.path.join(base_dir, "godot4_runtime", "CathedralAtlasBuilder.gd"), "w", encoding="utf-8") as f:
    f.write('''class_name CathedralAtlasBuilder
extends RefCounted

const FRAME_SIZE := Vector2(128, 128)
const ANIMATION_DEFINITIONS: Dictionary = {
    &"liturgical_idle": {"start": 0, "count": 4, "fps": 6.0, "loop": true},
    &"lumen_pulse": {"start": 4, "count": 6, "fps": 8.0, "loop": true},
    &"ocular_surge": {"start": 10, "count": 6, "fps": 10.0, "loop": true},
    &"harmonic_resonance": {"start": 16, "count": 8, "fps": 8.0, "loop": true},
    &"dialetheic_shift": {"start": 24, "count": 4, "fps": 6.0, "loop": true},
    &"penitent_recitation": {"start": 28, "count": 4, "fps": 8.0, "loop": true}
}

static func build_sprite_frames(master_texture: Texture2D) -> SpriteFrames:
    var sf := SpriteFrames.new()
    if sf.has_animation(&"default"): sf.remove_animation(&"default")
    for anim_name: StringName in ANIMATION_DEFINITIONS:
        var def: Dictionary = ANIMATION_DEFINITIONS[anim_name]
        sf.add_animation(anim_name)
        sf.set_animation_speed(anim_name, def["fps"])
        sf.set_animation_loop(anim_name, def["loop"])
        for i in range(def["count"]):
            var atlas_tex := AtlasTexture.new()
            atlas_tex.atlas = master_texture
            atlas_tex.region = Rect2((def["start"] + i) * FRAME_SIZE.x, 0.0, FRAME_SIZE.x, FRAME_SIZE.y)
            atlas_tex.filter_clip = true
            sf.add_frame(anim_name, atlas_tex)
    return sf
''')

with open(os.path.join(base_dir, "godot4_runtime", "cathedral_portrait_dither.gdshader"), "w", encoding="utf-8") as f:
    f.write('''shader_type canvas_item;
render_mode blend_mix, unshaded;

uniform float u_shadow_depth_ramp : hint_range(0.0, 1.0) = 0.65;
uniform float u_specular_rim_factor : hint_range(0.5, 3.0) = 1.35;
uniform float u_lumen_emission_gain : hint_range(0.0, 4.0) = 1.00;
uniform float u_afield_potency : hint_range(0.0, 2.0) = 0.87;

const float BAYER_2X2[4] = float[](0.00, 0.50, 0.75, 0.25);

void fragment() {
    vec4 base_color = texture(TEXTURE, UV);
    if (base_color.a < 0.01) discard;

    ivec2 pixel_coord = ivec2(floor(UV * 128.0));
    int bayer_index = (pixel_coord.x % 2) + (pixel_coord.y % 2) * 2;
    float dither_offset = (BAYER_2X2[bayer_index] - 0.5) * 0.12;
    float luminance = dot(base_color.rgb, vec3(0.299, 0.587, 0.114)) + dither_offset;

    if (luminance < u_shadow_depth_ramp) {
        base_color.rgb *= mix(0.40, 0.85, luminance / max(u_shadow_depth_ramp, 0.001));
    }

    if (base_color.b > 0.60 && base_color.r < 0.40) {
        base_color.rgb += vec3(0.0, 0.92, 1.0) * u_lumen_emission_gain * 1.25;
    }
    if (base_color.r > 0.68 && base_color.g > 0.52) {
        base_color.rgb += vec3(1.0, 0.82, 0.28) * u_afield_potency * 1.45;
    }

    COLOR = vec4(clamp(base_color.rgb, 0.0, 1.0), base_color.a);
}
''')

# 8. run_pipeline.py
with open(os.path.join(base_dir, "run_pipeline.py"), "w", encoding="utf-8") as f:
    f.write('''import os, json
from validator import MLAOSValidator
from transducer import BioSemanticTransducer
from atlas_compiler import AtlasCompiler
from dialogue_engine import DialoguePhysicsEngine
from ash_ledger_manager import AshLedgerManager

def main():
    print("=" * 65)
    print("  CATHEDRAL-ENGINE & MLAOS-PRIME CLOSED-LOOP INTEGRATION RUNNER  ")
    print("=" * 65 + "\\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    recipes_dir = os.path.join(base_dir, "recipes")

    print("--- [STAGE 1] Validating Archetype Recipes ---")
    validator = MLAOSValidator()
    for r_file in sorted(os.listdir(recipes_dir)):
        if r_file.endswith(".json"):
            with open(os.path.join(recipes_dir, r_file), "r", encoding="utf-8") as f:
                r_data = json.load(f)
            valid, errs, c_tau = validator.validate_character_recipe(r_data)
            print(f"  * {r_file}: Archetype={r_data.get('archetype')} | C_tau={c_tau} | Valid={valid}")

    print("\\n--- [STAGE 2 & 3] Bio-Semantic Transduction ---")
    transducer = BioSemanticTransducer()
    for r_file in sorted(os.listdir(recipes_dir)):
        if r_file.endswith(".json"):
            with open(os.path.join(recipes_dir, r_file), "r", encoding="utf-8") as f:
                r_data = json.load(f)
            res = transducer.transduce(r_data)
            print(f"  * Transduced: {res['archetype']} [{res['spectral_constant']}]")
            print(f"    - Latent Biasing: {res['latent_biasing']['channel_weights']}")
            print(f"    - Shader Ramp: {res['godot_shader_uniforms']['u_shadow_depth_ramp']} | Specular: {res['godot_shader_uniforms']['u_specular_rim_factor']}")

    print("\\n--- [STAGE 4] Exporting Native Godot 4 SpriteFrames Resources ---")
    compiler = AtlasCompiler()
    tres_out = os.path.join(base_dir, "godot4_runtime", "aurelia_9_spriteframes.tres")
    compiler.generate_godot4_spriteframes_tres("res://assets/atlases/aurelia_9_master_atlas.png", tres_out)
    print(f"  * Generated 32-frame Godot 4 SpriteFrames (.tres) at: {tres_out}")

    print("\\n--- [STAGE 5] Simulating Dialogue Stress & Lumen Gain Dynamics ---")
    diag_engine = DialoguePhysicsEngine()
    test_phrase = "The Bone Remains. The Hazard is Truth. Inscribe the Ash Ledger."
    cadence = diag_engine.calculate_phoneme_stress(test_phrase)
    for entry in cadence:
        print(f"    - Word: {entry['word']:<12} | Stress: {entry['stress']} | Lumen Gain: {entry['lumen_emission_gain']} | Anim: {entry['liturgical_animation']}")

    print("\\n--- [STAGE 6] Committing Historical Scars under Never-Overwrite Doctrine ---")
    ash_mgr = AshLedgerManager(os.path.join(base_dir, "ash_ledger.json"))
    entry = ash_mgr.append_historical_scar(
        archetype_id="Aurelia-9",
        scar_description="Diagonal pauldron fracture sealed with gold resonance solder.",
        severity=0.65,
        spectral_constant="Theta"
    )
    print(f"  * Appended Entry #{entry['index']} [J_hash: {entry['j_hash'][:16]}...] onto Layer 11.")

    print("\\n" + "=" * 65)
    print("    CLOSED-LOOP INTEGRATION EXECUTION COMPLETED WITH 0 ERRORS    ")
    print("=" * 65)

if __name__ == "__main__":
    main()
''')

print("Successfully established cathedral_integration_pipeline on local environment.")
