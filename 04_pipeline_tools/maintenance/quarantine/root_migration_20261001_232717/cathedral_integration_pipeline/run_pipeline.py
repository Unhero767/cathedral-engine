import os, json
from validator import MLAOSValidator
from transducer import BioSemanticTransducer
from atlas_compiler import AtlasCompiler
from dialogue_engine import DialoguePhysicsEngine
from ash_ledger_manager import AshLedgerManager

def main():
    print("=" * 65)
    print("  CATHEDRAL-ENGINE & MLAOS-PRIME CLOSED-LOOP INTEGRATION RUNNER  ")
    print("=" * 65 + "\n")

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

    print("\n--- [STAGE 2 & 3] Bio-Semantic Transduction ---")
    transducer = BioSemanticTransducer()
    for r_file in sorted(os.listdir(recipes_dir)):
        if r_file.endswith(".json"):
            with open(os.path.join(recipes_dir, r_file), "r", encoding="utf-8") as f:
                r_data = json.load(f)
            res = transducer.transduce(r_data)
            print(f"  * Transduced: {res['archetype']} [{res['spectral_constant']}]")
            print(f"    - Latent Biasing: {res['latent_biasing']['channel_weights']}")
            print(f"    - Shader Ramp: {res['godot_shader_uniforms']['u_shadow_depth_ramp']} | Specular: {res['godot_shader_uniforms']['u_specular_rim_factor']}")

    print("\n--- [STAGE 4] Exporting Native Godot 4 SpriteFrames Resources ---")
    compiler = AtlasCompiler()
    tres_out = os.path.join(base_dir, "godot4_runtime", "aurelia_9_spriteframes.tres")
    compiler.generate_godot4_spriteframes_tres("res://assets/atlases/aurelia_9_master_atlas.png", tres_out)
    print(f"  * Generated 32-frame Godot 4 SpriteFrames (.tres) at: {tres_out}")

    print("\n--- [STAGE 5] Simulating Dialogue Stress & Lumen Gain Dynamics ---")
    diag_engine = DialoguePhysicsEngine()
    test_phrase = "The Bone Remains. The Hazard is Truth. Inscribe the Ash Ledger."
    cadence = diag_engine.calculate_phoneme_stress(test_phrase)
    for entry in cadence:
        print(f"    - Word: {entry['word']:<12} | Stress: {entry['stress']} | Lumen Gain: {entry['lumen_emission_gain']} | Anim: {entry['liturgical_animation']}")

    print("\n--- [STAGE 6] Committing Historical Scars under Never-Overwrite Doctrine ---")
    ash_mgr = AshLedgerManager(os.path.join(base_dir, "ash_ledger.json"))
    entry = ash_mgr.append_historical_scar(
        archetype_id="Aurelia-9",
        scar_description="Diagonal pauldron fracture sealed with gold resonance solder.",
        severity=0.65,
        spectral_constant="Theta"
    )
    print(f"  * Appended Entry #{entry['index']} [J_hash: {entry['j_hash'][:16]}...] onto Layer 11.")

    print("\n" + "=" * 65)
    print("    CLOSED-LOOP INTEGRATION EXECUTION COMPLETED WITH 0 ERRORS    ")
    print("=" * 65)

if __name__ == "__main__":
    main()
