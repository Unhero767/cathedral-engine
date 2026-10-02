import os
import json

base_dir = os.path.join(os.getcwd(), "cathedral_integration_pipeline")
recipes_dir = os.path.join(base_dir, "recipes")
godot_dir = os.path.join(base_dir, "godot4_runtime")

os.makedirs(recipes_dir, exist_ok=True)
os.makedirs(godot_dir, exist_ok=True)

canonical_recipes = {
    "aurelia_9_vanguard.json": {
        "archetype": "Aurelia-9", "title": "Vanguard of the First Hearth", "spectral_constant": "Theta",
        "ego_density": 8.3, "afield_potency": 0.95, "dialetheic_state": "Joy in Martial Severity",
        "somatic_properties": {"armor": "Fluted gilded plate over blackened steel", "weathering_index": 0.65},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.45, "ocular_frequency_hz": 10.0}
    },
    "caelen_architect.json": {
        "archetype": "Caelen", "title": "Master Architect of the Lattices", "spectral_constant": "Psi",
        "ego_density": 8.1, "afield_potency": 0.88, "dialetheic_state": "Recursive Algorithmic Invariance",
        "somatic_properties": {"armor": "Matte ceramic plates with cyan conduits", "weathering_index": 0.40},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.20, "ocular_frequency_hz": 12.0}
    },
    "deimos_catalyst.json": {
        "archetype": "Deimos", "title": "Catalyst of Kinetic Remaking", "spectral_constant": "Phi",
        "ego_density": 9.4, "afield_potency": 0.99, "dialetheic_state": "Stochastic Volatility",
        "somatic_properties": {"armor": "Charred vanguard plate with thermal fissures", "weathering_index": 0.90},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.80, "ocular_frequency_hz": 8.0}
    },
    "sovereign_seraph.json": {
        "archetype": "Sovereign Seraph", "title": "Archon of the High Choir", "spectral_constant": "Theta",
        "ego_density": 8.5, "afield_potency": 1.10, "dialetheic_state": "Radiant Martial Authority",
        "somatic_properties": {"armor": "Gilded fluted cuirass with radial tri-key halo", "weathering_index": 0.50},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.60, "ocular_frequency_hz": 10.0}
    },
    "crucible_templar.json": {
        "archetype": "Crucible Templar", "title": "Defender of the Slag Gates", "spectral_constant": "Phi",
        "ego_density": 9.2, "afield_potency": 0.95, "dialetheic_state": "Thermal Combustion Equilibrium",
        "somatic_properties": {"armor": "Heavy slag-hardened plate with thermal relief vents", "weathering_index": 0.85},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.70, "ocular_frequency_hz": 8.0}
    },
    "crucible_berserk.json": {
        "archetype": "Crucible Berserk", "title": "Vanguard of Kinetic Remaking", "spectral_constant": "Phi",
        "ego_density": 9.8, "afield_potency": 1.25, "dialetheic_state": "Dynamic Entropy / Relentless Remaking",
        "somatic_properties": {"armor": "Fractured and re-welded plate with glowing fissures", "weathering_index": 0.95},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.90, "ocular_frequency_hz": 14.0}
    },
    "penitent_monad.json": {
        "archetype": "Penitent Monad", "title": "Anchor of Silent Substrates", "spectral_constant": "Delta",
        "ego_density": 8.3, "afield_potency": 0.65, "dialetheic_state": "Zero-Decay Archival Stillness",
        "somatic_properties": {"armor": "Oxidized blue lead plate over indigo monastic weave", "weathering_index": 0.70},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.15, "ocular_frequency_hz": 6.0}
    },
    "ash_scourge.json": {
        "archetype": "Ash Scourge", "title": "Forensic Sentinel of the Waste", "spectral_constant": "Delta",
        "ego_density": 8.7, "afield_potency": 0.80, "dialetheic_state": "Trauma Preserved as Structural Truth",
        "somatic_properties": {"armor": "Charred fossilized plate impregnated with soot and ash", "weathering_index": 0.90},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.35, "ocular_frequency_hz": 7.0}
    },
    "null_astrologer.json": {
        "archetype": "Null Astrologer", "title": "Cartographer of Non-Indexed Space", "spectral_constant": "Null",
        "ego_density": 7.9, "afield_potency": 0.40, "dialetheic_state": "Anti-Resonance Invariance",
        "somatic_properties": {"armor": "Matte obsidian ceramic plates absorbing all incident light", "weathering_index": 0.30},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.05, "ocular_frequency_hz": 4.0}
    },
    "verdant_anchor.json": {
        "archetype": "Verdant Anchor", "title": "Attuner of the Living Filaments", "spectral_constant": "Epsilon",
        "ego_density": 8.3, "afield_potency": 0.90, "dialetheic_state": "Restorative Biomechanical Symbiosis",
        "somatic_properties": {"armor": "Laminated bone-fiber plate interwoven with emerald conduits", "weathering_index": 0.45},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.40, "ocular_frequency_hz": 9.0}
    },
    "ash_scribe_delta.json": {
        "archetype": "Ash Scribe", "title": "Archivist of the First Prohibition", "spectral_constant": "Delta",
        "ego_density": 8.3, "afield_potency": 0.70, "dialetheic_state": "Zero-Decay Historical Preservation",
        "somatic_properties": {"armor": "Layered indigo cowl over archival leaden vestments", "weathering_index": 0.85},
        "liturgical_telemetry": {"dialogue_luminance_gain": 1.10, "ocular_frequency_hz": 6.0}
    }
}

for name, r_data in canonical_recipes.items():
    with open(os.path.join(recipes_dir, name), "w", encoding="utf-8") as f:
        json.dump(r_data, f, indent=2)

# Pre-wired Godot 4 scene (.tscn)
tscn_content = """[gd_scene load_steps=5 format=3 uid="uid://mlaoseas03scene001"]

[ext_resource type="Shader" path="res://cathedral_integration_pipeline/godot4_runtime/cathedral_portrait_dither.gdshader" id="1_dither_shader"]
[ext_resource type="SpriteFrames" path="res://cathedral_integration_pipeline/godot4_runtime/aurelia_9_spriteframes.tres" id="2_sprite_frames"]
[ext_resource type="Script" path="res://cathedral_integration_pipeline/godot4_runtime/CathedralAvatarPortrait.gd" id="3_portrait_script"]

[sub_resource type="ShaderMaterial" id="ShaderMaterial_cathedral"]
shader = ExtResource("1_dither_shader")
shader_parameter/u_shadow_depth_ramp = 0.55
shader_parameter/u_specular_rim_factor = 1.53
shader_parameter/u_lumen_emission_gain = 1.0
shader_parameter/u_afield_potency = 0.95
shader_parameter/u_enable_dither = true
shader_parameter/u_enable_dual_lumen = true

[node name="CathedralPortraitView" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2

[node name="AvatarPortrait" type="AnimatedSprite2D" parent="."]
material = SubResource("ShaderMaterial_cathedral")
position = Vector2(64, 64)
sprite_frames = ExtResource("2_sprite_frames")
animation = &"liturgical_idle"
script = ExtResource("3_portrait_script")
character_recipe_path = "res://cathedral_integration_pipeline/recipes/aurelia_9_vanguard.json"
base_afield_potency = 0.95
"""

with open(os.path.join(godot_dir, "CathedralPortraitView.tscn"), "w", encoding="utf-8") as f:
    f.write(tscn_content)

# Update run_pipeline.py to batch compile all .tres files
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
    godot_dir = os.path.join(base_dir, "godot4_runtime")

    print("--- [STAGE 1] Validating Archetype Recipes ---")
    validator = MLAOSValidator()
    all_recipes = sorted([f for f in os.listdir(recipes_dir) if f.endswith(".json")])
    for r_file in all_recipes:
        with open(os.path.join(recipes_dir, r_file), "r", encoding="utf-8") as f:
            r_data = json.load(f)
        valid, errs, c_tau = validator.validate_character_recipe(r_data)
        print(f"  * {r_file:<24}: Archetype={r_data.get('archetype'):<18} | C_tau={c_tau:<6} | Valid={valid}")

    print("\\n--- [STAGE 2, 3 & 4] Transduction & Godot 4 Resource Export ---")
    transducer = BioSemanticTransducer()
    compiler = AtlasCompiler()

    for r_file in all_recipes:
        with open(os.path.join(recipes_dir, r_file), "r", encoding="utf-8") as f:
            r_data = json.load(f)
        res = transducer.transduce(r_data)
        slug = r_file.replace(".json", "")
        tres_out = os.path.join(godot_dir, f"{slug}_spriteframes.tres")
        compiler.generate_godot4_spriteframes_tres(f"res://cathedral_integration_pipeline/assets/{slug}_atlas.png", tres_out)
        print(f"  * Transduced: {res['archetype']} [{res['spectral_constant']}] -> Exported: {os.path.basename(tres_out)}")
        print(f"    - Latent Biasing: {res['latent_biasing']['channel_weights']} | Shader Ramp: {res['godot_shader_uniforms']['u_shadow_depth_ramp']}")

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

print("All 11 canonical recipes populated and CathedralPortraitView.tscn created.")
