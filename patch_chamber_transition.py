#!/usr/bin/env python3
import os
import re

ENGINE_PATH = "/users/kennethdallmier/cathedral_engine/02_engine_core/logic_engines/game_loop_engine.py"

with open(ENGINE_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Define Chamber Manifests if not already present
if "CHAMBER_MANIFESTS = {" not in code:
    manifest_block = '''
CHAMBER_MANIFESTS = {
    1: {
        "name": "Chamber I: The Lithic Threshold",
        "stratum": "Prime Foundations",
        "carrier_hz": 42.00,
        "temperature_k": 293.15,
        "pressure_bar": 1.01,
        "spectral_dominant": "Gold/Joy (580nm)",
        "cryo_flow_rate_l_min": 0.0,
        "portal_exit": (7, 7),
        "description": "Basaltic bedrock foundation; 42.0 Hz carrier baseline."
    },
    2: {
        "name": "Chamber II: Consciousness Intersections and Somatic Heat Sink",
        "stratum": "Prime Foundations",
        "carrier_hz": 52.80,
        "temperature_k": 77.35,
        "pressure_bar": 2.10,
        "spectral_dominant": "Teal/Curiosity (495nm) × Blue/Memory (470nm)",
        "cryo_flow_rate_l_min": 9.4,
        "portal_exit": (7, 7),
        "description": "Liquid nitrogen cryogenic manifold; 52.8 Hz somatic heat sink."
    }
}
'''
    # Insert after GameState enum
    insert_pos = code.find("class GameState(str, Enum):")
    if insert_pos != -1:
        end_enum = code.find("\n\n", insert_pos)
        code = code[:end_enum] + "\n" + manifest_block + code[end_enum:]
        print("✓ Injected CHAMBER_MANIFESTS into game_loop_engine.py")

# 2. Add transition_to_chamber method
if "def transition_to_chamber" not in code:
    transition_method = '''
    def transition_to_chamber(self, target_chamber_index: int, entry_x: int = 4, entry_y: int = 4) -> Dict[str, Any]:
        """
        Executes an isomorphic spatial transition between consecrated chambers.
        Updates spatial coordinates, thermodynamic telemetry, carrier frequency,
        and spectral dominant, appending the transition record to the Ash Archive.
        """
        if target_chamber_index not in CHAMBER_MANIFESTS:
            return {"error": f"Invalid chamber index {target_chamber_index}."}
        
        prev_chamber = self.player.chamber_index
        target_manifest = CHAMBER_MANIFESTS[target_chamber_index]
        
        self.player.chamber_index = target_chamber_index
        self.player.active_stratum = target_manifest["stratum"]
        self.player.x = entry_x
        self.player.y = entry_y
        self.player.current_ap = self.player.max_ap
        
        # Attune emotional state and spectrum if transitioning into Chamber II
        if target_chamber_index == 2:
            self.player.spectrum_affinity = EnemySpectrum.TEAL
            self.player.emotional_state = "Teal/Curiosity (Somatic Attuned)"
        
        log_msg = (
            f"🌀 CHAMBER TRANSITION: Exited Chamber {prev_chamber} -> Inscribed into "
            f"{target_manifest['name']} at ({entry_x}, {entry_y}). "
            f"[Carrier: {target_manifest['carrier_hz']:.1f} Hz | "
            f"Temp: {target_manifest['temperature_k']:.2f} K ({target_manifest['temperature_k'] - 273.15:.1f} °C) | "
            f"Pressure: {target_manifest['pressure_bar']:.2f} bar | "
            f"Spectrum: {target_manifest['spectral_dominant']}]"
        )
        self.action_log.append(log_msg)
        
        # Clear previous combat squad and restore exploration
        self.active_combat_squad = []
        self.state = GameState.EXPLORATION
        
        # Record to Paraconsistent ledger / Ash Archive under Lex I
        try:
            self.paraconsistent.process_frame_tick(self.turn_counter, c_pos=0.85, c_neg=0.15)
        except Exception:
            pass
            
        return self.get_full_game_state()
'''
    insert_before = code.find("    def start_new_game(")
    if insert_before != -1:
        code = code[:insert_before] + transition_method + "\n" + code[insert_before:]
        print("✓ Added transition_to_chamber() to GameLoopEngine")

# 3. Patch player_move to trigger transition on reaching (7, 7)
portal_trigger_code = '''
        # Portal check: stepping on chamber exit threshold (7, 7)
        if self.state == GameState.EXPLORATION and (target_x, target_y) == (7, 7):
            next_chamber = self.player.chamber_index + 1
            if next_chamber in CHAMBER_MANIFESTS:
                self.action_log.append(f"Threshold portal reached at (7, 7). Advancing to Chamber {next_chamber}...")
                return self.transition_to_chamber(next_chamber, entry_x=4, entry_y=4)
'''
if "Threshold portal reached at (7, 7)" not in code:
    move_return = code.find("        return self.get_full_game_state()", code.find("def player_move("))
    if move_return != -1:
        code = code[:move_return] + portal_trigger_code + "\n" + code[move_return:]
        print("✓ Integrated portal trigger logic into player_move()")

with open(ENGINE_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("=== [Chamber Transition Integration Complete] ===")
