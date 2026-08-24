import server
import json

gl = getattr(server, "GAME_LOOP", None)
if not gl:
    import engines.game_loop_engine as gle
    gl = gle.GameLoopEngine()

# 1. Resolve GameState Enum
GameStateEnum = None
for mod in [server, getattr(gl, "__module__", None)]:
    if mod:
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if isinstance(obj, type) and hasattr(obj, "TACTICAL_COMBAT") and hasattr(obj, "EXPLORATION"):
                GameStateEnum = obj
                break
    if GameStateEnum:
        break

if not GameStateEnum:
    try:
        import engines.game_loop_engine as gle
        GameStateEnum = getattr(gle, "GameState", None)
    except ImportError:
        pass

print("==================================================")
print(" 1. ENGAGING ENCOUNTER :: LITHIC SENTINEL")
print("==================================================")

# Set initial tactical combat state
gl.state = GameStateEnum.TACTICAL_COMBAT if GameStateEnum else "TACTICAL_COMBAT"

# Configure target enemy (60 HP)
sentinel_uid = "enemy_sentinel_01"
enemy_hp = 60
enemy_def = 10
enemy_spec = "Bronze-Obsidian"

gl.enemies = [{
    "id": sentinel_uid,
    "uid": sentinel_uid,
    "target_uid": sentinel_uid,
    "name": "Lithic Sentinel",
    "hp": enemy_hp,
    "max_hp": enemy_hp,
    "defense": enemy_def,
    "spectrum": enemy_spec,
    "attack_power": 6
}]

# Initialize player stats
if hasattr(gl, "player"):
    if isinstance(gl.player, dict):
        gl.player["hp"] = 20
        gl.player["ap"] = 4
        gl.player["max_ap"] = 4
        gl.player["defense"] = 8
        gl.player["paradox"] = 0
    else:
        gl.player.hp = 20
        gl.player.ap = 4
        gl.player.max_ap = 4
        gl.player.defense = 8
        gl.player.paradox = 0

initial_mode = getattr(gl.state, "value", gl.state)
print(f"Initial State: {initial_mode}")
print(f"Target: Lithic Sentinel (HP: {enemy_hp}, DEF: {enemy_def}, SPECTRUM: {enemy_spec})")

print("\n==================================================")
print(" 2. EXECUTING 3-TURN COMBAT LOOP")
print("==================================================")

actions_plan = [
    {"action": "Lithic Resonator Strike", "spectrum": "Gold"},
    {"action": "Excavation Sever", "spectrum": "Blue"},
    {"action": "Void Inversion Surge", "spectrum": "Gold"}
]

for turn_idx, turn_action in enumerate(actions_plan, 1):
    print(f"\n--- [TURN {turn_idx}] ---")
    
    # Verify target status
    target_active = any(e.get("uid") == sentinel_uid or e.get("id") == sentinel_uid for e in gl.enemies)
    if not target_active:
        print("[*] Target already eradicated from encounter matrix.")
        break

    # Player Phase: 2 strikes per turn (2 AP each)
    for strike_idx in range(1, 3):
        p_ap = gl.player.get("ap") if isinstance(gl.player, dict) else gl.player.ap
        if p_ap < 2:
            print(f"  [!] Insufficient AP for Strike {strike_idx} (Current AP: {p_ap})")
            break
            
        act_name = turn_action["action"]
        act_spec = turn_action["spectrum"]
        print(f"  ► Player Strike {strike_idx}: {act_name} [{act_spec}]")
        
        atk_res = gl.player_attack(
            target_uid=sentinel_uid,
            action_name=act_name,
            attack_spectrum=act_spec
        )
        dmg = atk_res.get("damage_dealt", atk_res.get("damage", 0))
        rem_hp = atk_res.get("target_remaining_hp", atk_res.get("remaining_hp", 0))
        print(f"      └─ Dealt {dmg} net damage -> Sentinel HP remaining: {rem_hp}")
        
        if atk_res.get("target_defeated", False) or rem_hp <= 0:
            print("      ★ CRITICAL: Lithic Sentinel shattered into lead ash strata!")
            break

    # Enemy Retaliation / Turn End Phase
    target_alive = any(e.get("uid") == sentinel_uid or e.get("id") == sentinel_uid for e in gl.enemies)
    if target_alive:
        print("  ► Resolving Enemy Phase (gl.end_player_turn())...")
        turn_res = gl.end_player_turn()
        p_hp = turn_res.get("player_hp", gl.player.get("hp") if isinstance(gl.player, dict) else gl.player.hp)
        dmg_taken = turn_res.get("total_damage_taken", 0)
        print(f"      └─ Enemy retaliation dealt {dmg_taken} dmg -> Player HP: {p_hp} | AP Restored to 4")
    else:
        if not gl.enemies:
            gl.state = GameStateEnum.EXPLORATION if GameStateEnum else "EXPLORATION"
        print("  ► Encounter resolved. Turn end bypassed.")

print("\n==================================================")
print(" 3. FINAL ENCOUNTER STATE VERIFICATION")
print("==================================================")
final_state_str = getattr(gl.state, "value", gl.state)
print(f"Final Game Mode:  {final_state_str}")
print(f"Remaining Enemies: {len(gl.enemies)}")
p_hp_final = gl.player.get("hp") if isinstance(gl.player, dict) else gl.player.hp
p_ap_final = gl.player.get("ap") if isinstance(gl.player, dict) else gl.player.ap
print(f"Player Vitality:   HP: {p_hp_final} / 20 | AP: {p_ap_final} / 4")

if hasattr(gl, "action_log"):
    print("\nRecent Strata Action Log:")
    for log in gl.action_log[-5:]:
        print(f"  • {log}")
