import re
import shutil

SERVER_FILE = "server.py"
BACKUP_FILE = "server.py.bak"

print("==================================================")
print(" CATHEDRAL-ENGINE :: COMBAT ROUTINES PATCHER")
print("==================================================")

# 1. Create a safety backup
shutil.copyfile(SERVER_FILE, BACKUP_FILE)
print(f"[+] Safety backup created at: {BACKUP_FILE}")

with open(SERVER_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 2. Ensure combat_matrix is imported
if "import combat_matrix" not in content:
    content = "import combat_matrix\n" + content
    print("[+] Added 'import combat_matrix' to server.py header.")
else:
    print("[*] 'import combat_matrix' already present.")

# 3. New implementation for player_attack
NEW_PLAYER_ATTACK = '''    def player_attack(self, target_uid: str, action_name: str, attack_spectrum="Gold") -> dict:
        if getattr(self, "state", getattr(self, "game_state", "")) != "TACTICAL_COMBAT":
            return {"error": "Combat action only valid in TACTICAL_COMBAT state."}

        player = getattr(self, "player", {})
        ap_cost = 2
        curr_ap = player.get("ap", 0) if isinstance(player, dict) else getattr(player, "ap", 0)
        if curr_ap < ap_cost:
            return {"error": "Insufficient Action Points (AP)."}

        # Find target in enemies list
        target = None
        enemies_list = getattr(self, "enemies", [])
        for e in enemies_list:
            e_uid = e.get("uid") if isinstance(e, dict) else getattr(e, "uid", None)
            if e_uid == target_uid:
                target = e
                break

        if not target:
            return {"error": f"Target {target_uid} not found."}

        # Normalize spectrum string/enum
        spec_str = str(getattr(attack_spectrum, "value", attack_spectrum))
        tgt_spec = target.get("spectrum", "Bronze-Obsidian") if isinstance(target, dict) else getattr(target, "spectrum", "Bronze-Obsidian")
        tgt_def = target.get("defense", 12) if isinstance(target, dict) else getattr(target, "defense", 12)

        # Compute mitigated damage via combat_matrix
        calc = combat_matrix.compute_mitigated_damage(
            base_potency=24,
            attacker_spectrum=spec_str,
            defender_spectrum=str(tgt_spec),
            defender_defense=int(tgt_def),
            is_carrier_aligned=(spec_str == "Gold")
        )

        dmg = calc["net_damage"]
        if isinstance(target, dict):
            target["hp"] = max(0, target.get("hp", 0) - dmg)
            t_hp = target["hp"]
            t_name = target.get("name", "Sentinel")
        else:
            target.hp = max(0, target.hp - dmg)
            t_hp = target.hp
            t_name = getattr(target, "name", "Sentinel")

        # Deduct AP
        if isinstance(player, dict):
            player["ap"] -= ap_cost
        else:
            player.ap -= ap_cost

        log_entry = f"Kiri deployed {action_name} [{spec_str}] -> Dealt {dmg} dmg to {t_name} ({calc['mitigation_percentage']}% mitigated)."
        if hasattr(self, "action_log"):
            self.action_log.append(log_entry)

        is_defeated = (t_hp <= 0)
        if is_defeated:
            if hasattr(self, "action_log"):
                self.action_log.append(f"{t_name} collapsed into ash strata.")
            if isinstance(enemies_list, list) and target in enemies_list:
                enemies_list.remove(target)
            if not enemies_list:
                if hasattr(self, "state"): self.state = "EXPLORATION"
                if hasattr(self, "game_state"): self.game_state = "EXPLORATION"

        return {
            "success": True,
            "action": action_name,
            "damage_dealt": dmg,
            "target_remaining_hp": t_hp,
            "target_defeated": is_defeated,
            "log": log_entry
        }'''

# 4. New implementation for end_player_turn
NEW_END_PLAYER_TURN = '''    def end_player_turn(self) -> dict:
        if getattr(self, "state", getattr(self, "game_state", "")) != "TACTICAL_COMBAT":
            return {"error": "End turn only available during combat."}

        player = getattr(self, "player", {})
        player_spec = player.get("spectrum", "Obsidian") if isinstance(player, dict) else getattr(player, "spectrum", "Obsidian")
        player_def = player.get("defense", 8) if isinstance(player, dict) else getattr(player, "defense", 8)
        paradox_strain = player.get("paradox", 0) if isinstance(player, dict) else getattr(player, "paradox", 0)
        strain_mod = 1.0 + (paradox_strain * combat_matrix.PARADOX_STRAIN_RETALIATION_RATE)

        retaliation_events = []
        total_dmg = 0
        enemies_list = getattr(self, "enemies", [])

        for enemy in list(enemies_list):
            e_hp = enemy.get("hp", 0) if isinstance(enemy, dict) else getattr(enemy, "hp", 0)
            if e_hp <= 0:
                continue

            e_spec = enemy.get("spectrum", "Bronze-Obsidian") if isinstance(enemy, dict) else getattr(enemy, "spectrum", "Bronze-Obsidian")
            e_atk = enemy.get("attack_power", 14) if isinstance(enemy, dict) else getattr(enemy, "attack_power", 14)
            e_name = enemy.get("name", "Enemy") if isinstance(enemy, dict) else getattr(enemy, "name", "Enemy")

            calc = combat_matrix.compute_mitigated_damage(
                base_potency=int(e_atk),
                attacker_spectrum=str(e_spec),
                defender_spectrum=str(player_spec),
                defender_defense=int(player_def),
                strain_mod=strain_mod
            )

            dmg = calc["net_damage"]
            total_dmg += dmg

            if isinstance(player, dict):
                player["hp"] = max(0, player.get("hp", 20) - dmg)
            else:
                player.hp = max(0, player.hp - dmg)

            event_msg = f"{e_name} retaliated [{e_spec}] -> Dealt {dmg} damage to Kiri."
            retaliation_events.append(event_msg)
            if hasattr(self, "action_log"):
                self.action_log.append(event_msg)

        # Replenish AP & advance turn counter
        if hasattr(self, "turn"):
            self.turn += 1
        if isinstance(player, dict):
            player["ap"] = player.get("max_ap", 4)
            final_hp = player["hp"]
        else:
            player.ap = getattr(player, "max_ap", 4)
            final_hp = player.hp

        return {
            "turn": getattr(self, "turn", 1),
            "retaliation_events": retaliation_events,
            "total_damage_taken": total_dmg,
            "player_hp": final_hp,
            "player_ap_restored": player.get("ap") if isinstance(player, dict) else player.ap,
            "combat_status": "DEFEAT" if final_hp <= 0 else "ACTIVE"
        }'''

# 5. Regex-replace methods inside GameLoopEngine
pattern_attack = r"    def player_attack\(self,[\s\S]*?(?=\n    def |\nclass |\Z)"
pattern_turn = r"    def end_player_turn\(self[\s\S]*?(?=\n    def |\nclass |\Z)"

if re.search(pattern_attack, content):
    content = re.sub(pattern_attack, NEW_PLAYER_ATTACK + "\n", content, count=1)
    print("[+] Patched def player_attack() in server.py.")
else:
    print("[-] Warning: Existing player_attack() signature not matched for inline replacement.")

if re.search(pattern_turn, content):
    content = re.sub(pattern_turn, NEW_END_PLAYER_TURN + "\n", content, count=1)
    print("[+] Patched def end_player_turn() in server.py.")
else:
    print("[-] Warning: Existing end_player_turn() signature not matched for inline replacement.")

with open(SERVER_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("\n[+] Patch complete. Verifying Python compilation...")
import py_compile
py_compile.compile(SERVER_FILE, doraise=True)
print("[+] server.py syntax verification passed.")
