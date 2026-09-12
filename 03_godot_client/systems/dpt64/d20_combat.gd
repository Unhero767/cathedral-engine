class_name D20Combat
extends RefCounted

static func resolve_attack(attacker_str: int, target_ac: int, weapon_bonus: int) -> Dictionary:
    var rng = RandomNumberGenerator.new()
    rng.randomize()
    var roll = rng.randi_range(1, 20)
    var mod = floor((attacker_str - 10) / 2.0)
    var total_attack = roll + mod + weapon_bonus
    
    var is_crit = (roll == 20)
    var is_fumble = (roll == 1)
    var hit = (total_attack >= target_ac and not is_fumble) or is_crit
    
    return {
        "roll": roll,
        "modifier": mod,
        "total": total_attack,
        "hit": hit,
        "crit": is_crit,
        "fumble": is_fumble
    }
