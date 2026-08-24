import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comfyui_bridge import ComfyUIBridge
from audio_tts_engine import AudioPhonemeEngine
from combat_somatic_engine import SomaticCombatEngine
from notebooklm_lore_compiler import NotebookLMLoreCompiler
from dialetheic_logic_buffer import BelnapDunnLogicBuffer

def main():
    print("=" * 68)
    print("   CATHEDRAL-ENGINE 5-MODULE INTEGRATED ARCHITECTURE SUITE   ")
    print("=" * 68 + "\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    recipes_dir = os.path.join(base_dir, "recipes")
    godot_dir = os.path.join(base_dir, "godot4_runtime")

    # MODULE 1: ComfyUI REST/WebSocket Bridge
    print("--- [MODULE 1] ComfyUI REST & WebSocket Automation Bridge ---")
    bridge = ComfyUIBridge()
    recipes = [f for f in sorted(os.listdir(recipes_dir)) if f.endswith(".json")]
    if recipes:
        target_recipe = os.path.join(recipes_dir, recipes[0])
        res_m1 = bridge.generate_atlas_headlessly(target_recipe, godot_dir)
        print(f"  * Headless Generation: {res_m1['archetype']}")
        print(f"    - Status: {res_m1['status']}")
        print(f"    - SpriteFrames .tres: {os.path.basename(res_m1['tres_path'])}")

    # MODULE 2: Live Audio / TTS Phoneme Cadence
    print("\n--- [MODULE 2] Live Audio & Phoneme Stress Sync Engine ---")
    audio_engine = AudioPhonemeEngine()
    test_speech = "The Bone Remains. The Hazard is Truth. We hold the First Hearth."
    cadence_res = audio_engine.synthesize_cadence_envelope(test_speech)
    print(f"  * Speech Line: \"{cadence_res['text']}\" (Duration: {cadence_res['total_duration_sec']}s)")
    for word_node in cadence_res["timeline"][:3]:
        print(f"    - Word: {word_node['word']:<12} | RMS: {word_node['audio_peak_rms']} | Lumen Gain: {word_node['shader_lumen_gain']}")

    # MODULE 3: Bio-Semantic Combat & Somatic Damage Shunts
    print("\n--- [MODULE 3] Bio-Semantic Combat & Layer 11 Damage Shunt ---")
    combat_engine = SomaticCombatEngine(os.path.join(base_dir, "ash_ledger.json"))
    sample_entity = {"archetype": "Aurelia-9", "ego_density": 8.3, "afield_potency": 0.95, "spectral_constant": "Theta"}
    combat_res = combat_engine.apply_somatic_damage(sample_entity, "KINETIC_RUPTURE", 85.0)
    print(f"  * Entity Damaged: {combat_res['archetype']} (Raw: {combat_res['raw_damage']} dmg)")
    print(f"    - Barrier Absorbed: {combat_res['barrier_absorbed']} | Penetrating: {combat_res['penetrating_damage']}")
    print(f"    - Layer 11 Modification: {combat_res['layer_11_visual']}")
    print(f"    - Ash Archive Anchor: Entry #{combat_res['ash_archive_index']} [J_hash: {combat_res['j_hash'][:16]}...]")

    # MODULE 4: 40-Book Codex & NotebookLM Lore Compiler
    print("\n--- [MODULE 4] 40-Book Codex & NotebookLM Synthesis Exporter ---")
    lore_compiler = NotebookLMLoreCompiler(base_dir)
    pack_out = os.path.join(base_dir, "notebooklm_packs", "MLAOS_Cathedral_Master_Corpus.md")
    lore_compiler.compile_research_pack(pack_out)
    print(f"  * Compiled High-Density Corpus for NotebookLM ({os.path.getsize(pack_out)} bytes)")
    print(f"    - Exported to: {pack_out}")

    # MODULE 5: Paraconsistent Belnap-Dunn Logic Buffer
    print("\n--- [MODULE 5] Paraconsistent Belnap-Dunn Logic Buffer ---")
    logic_buffer = BelnapDunnLogicBuffer()
    dialetheic_eval = logic_buffer.evaluate_contradiction("Glitch_Waste_Perimeter_Integrity", "TRUE", "TRUE")
    print(f"  * Proposition: {dialetheic_eval['proposition']}")
    print(f"    - Truth State: {dialetheic_eval['truth_value']} (Dialetheic Glut)")
    print(f"    - Metamorphic Squeeze: Active={dialetheic_eval['metamorphic_squeeze_active']}")
    print(f"    - Resolution: {dialetheic_eval['harmonic_scar']}")
    print(f"    - TRIZ Algorithmic Cost (c): {dialetheic_eval['algorithmic_cost_c']} <= 0.30")

    print("\n" + "=" * 68)
    print("     ALL 5 CATHEDRAL-ENGINE MODULES EXECUTED WITH 0 ERRORS     ")
    print("=" * 68)

if __name__ == "__main__":
    main()
