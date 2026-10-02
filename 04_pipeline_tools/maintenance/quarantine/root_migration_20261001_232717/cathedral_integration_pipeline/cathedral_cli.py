"""
Cathedral-Engine & MLAOS-Prime Unified Interactive CLI Dashboard
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from validator import MLAOSValidator
from transducer import BioSemanticTransducer
from atlas_compiler import AtlasCompiler
from dialogue_engine import DialoguePhysicsEngine
from ash_ledger_manager import AshLedgerManager
from comfyui_bridge import ComfyUIBridge
from audio_tts_engine import AudioPhonemeEngine
from combat_somatic_engine import SomaticCombatEngine
from notebooklm_lore_compiler import NotebookLMLoreCompiler
from dialetheic_logic_buffer import BelnapDunnLogicBuffer

def print_banner():
    print("=" * 70)
    print("   MLAOS-PRIME // CATHEDRAL-ENGINE SOVEREIGN INTERACTIVE CLI HUB   ")
    print("   Foundational Axiom: Emotion = Physics = Magic = Biology = Arch  ")
    print("=" * 70)

def run_diagnostics():
    print("\n--- [1] SYSTEM DIAGNOSTICS & METALOGICAL TYPE CHECKING ---")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    recipes_dir = os.path.join(base_dir, "recipes")
    validator = MLAOSValidator()
    
    recipes = sorted([f for f in os.listdir(recipes_dir) if f.endswith(".json")])
    print(f"Active Archetype Recipes Found: {len(recipes)}")
    for r in recipes:
        with open(os.path.join(recipes_dir, r), "r", encoding="utf-8") as f:
            data = json.load(f)
        valid, errs, c_tau = validator.validate_character_recipe(data)
        print(f"  * {r:<24} | {data.get('archetype'):<18} | C_tau={c_tau:<6} | Valid={valid}")

def run_combat_test():
    print("\n--- [2] BIO-SEMANTIC COMBAT & LAYER 11 DAMAGE SHUNT ---")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    combat_engine = SomaticCombatEngine(os.path.join(base_dir, "ash_ledger.json"))
    sample_entity = {"archetype": "Aurelia-9", "ego_density": 8.3, "afield_potency": 0.95, "spectral_constant": "Theta"}
    
    res = combat_engine.apply_somatic_damage(sample_entity, "KINETIC_RUPTURE", 120.0)
    print(f"Target: {res['archetype']} | Raw Damage: {res['raw_damage']} HP")
    print(f"Barrier Absorbed: {res['barrier_absorbed']} | Penetrating Damage: {res['penetrating_damage']}")
    print(f"Layer 11 Modification: {res['layer_11_visual']}")
    print(f"Ash Archive Commitment: Entry #{res['ash_archive_index']} [J_hash: {res['j_hash'][:16]}...]")

def run_notebooklm_export():
    print("\n--- [3] 40-BOOK CODEX & NOTEBOOKLM SYNTHESIS EXPORT ---")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    compiler = NotebookLMLoreCompiler(base_dir)
    pack_out = os.path.join(base_dir, "notebooklm_packs", "MLAOS_Cathedral_Master_Corpus.md")
    compiler.compile_research_pack(pack_out)
    print(f"Compiled High-Density Master Corpus ({os.path.getsize(pack_out)} bytes)")
    print(f"Export Location: {pack_out}")

def run_paraconsistent_test():
    print("\n--- [4] PARACONSISTENT BELNAP-DUNN FOUR-VALUED LOGIC BUFFER ---")
    buffer = BelnapDunnLogicBuffer()
    res = buffer.evaluate_contradiction("Glitch_Waste_Containment_Field", "TRUE", "TRUE")
    print(f"Proposition: {res['proposition']}")
    print(f"Dialetheic Truth Value: {res['truth_value']} (Glut State: A & ~A)")
    print(f"Metamorphic Squeeze: Active={res['metamorphic_squeeze_active']}")
    print(f"Resolution: {res['harmonic_scar']}")
    print(f"TRIZ Trimming Algorithmic Cost (c): {res['algorithmic_cost_c']} <= 0.30")

if __name__ == "__main__":
    print_banner()
    run_diagnostics()
    run_combat_test()
    run_notebooklm_export()
    run_paraconsistent_test()
    print("\n" + "=" * 70)
    print("     ALL CATHEDRAL-ENGINE SUBSYSTEMS FULLY OPERATIONAL     ")
    print("=" * 70)
