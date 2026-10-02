import os, json
from dialogue_engine import DialoguePhysicsEngine
from ash_ledger_manager import AshLedgerManager

def run_simulation():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(base_dir, "narrative_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print("=" * 65)
    print("      MLAOS NARRATIVE & NPC INTERACTIVE DIALOGUE SIMULATOR      ")
    print("=" * 65 + "\n")

    npcs = manifest.get("npcs", {})
    print(f"--- Registered NPCs in Cathedral Engine ({len(npcs)}) ---")
    for npc_name, data in npcs.items():
        print(f"  * {npc_name:<12} [{data['spectral_constant']}] : {data['title']}")

    conv = manifest["conversations"]["chamber_01_prologue"]
    print(f"\n--- Running Conversation: \"{conv['title']}\" ---")
    
    nodes = conv["nodes"]
    current_node = conv["start_node"]
    diag_engine = DialoguePhysicsEngine()
    ash_mgr = AshLedgerManager(os.path.join(base_dir, "ash_ledger.json"))

    step = 1
    while current_node:
        node_data = nodes[current_node]
        speaker = node_data["speaker"]
        text = node_data["text"]
        liturgy = node_data.get("default_liturgy", "liturgical_idle")
        npc_info = npcs.get(speaker, {})

        print(f"\n[Turn {step}] Speaker: {speaker} ({npc_info.get('title', '')}) [{npc_info.get('spectral_constant', 'Theta')}]")
        print(f"  Liturgical State: {liturgy}")
        print(f"  Dialogue Line: \"{text}\"")

        cadence = diag_engine.calculate_phoneme_stress(text)
        max_stress_word = max(cadence, key=lambda x: x["stress"])
        print(f"  Peak Cadence: \"{max_stress_word['word']}\" (Stress: {max_stress_word['stress']}, Lumen Gain: {max_stress_word['lumen_emission_gain']}, Anim: {max_stress_word['liturgical_animation']})")

        if "choices" in node_data and node_data["choices"]:
            print("  Choices Presented:")
            for c_idx, choice in enumerate(node_data["choices"]):
                print(f"    [{c_idx + 1}] {choice['text']}")
            
            selected = node_data["choices"][0]
            print(f"  -> Selecting Choice: [1] {selected['text']}")
            
            entry = ash_mgr.append_historical_scar(
                archetype_id=speaker,
                scar_description=selected["ash_ledger_event"],
                severity=0.75,
                spectral_constant=npc_info.get("spectral_constant", "Theta")
            )
            print(f"  -> [Ash Archive] Committed Event #{entry['index']} [J_hash: {entry['j_hash'][:16]}...]")
            current_node = selected["next"]
        else:
            current_node = node_data.get("next")
        step += 1

    print("\n" + "=" * 65)
    print("          NARRATIVE SIMULATION COMPLETED SUCCESSFULLY           ")
    print("=" * 65)

if __name__ == "__main__":
    run_simulation()
