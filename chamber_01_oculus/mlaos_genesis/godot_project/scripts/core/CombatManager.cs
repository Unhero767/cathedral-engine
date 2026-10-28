using Godot;
using System;
using System.Collections.Generic;

public class MonsterEntity
{
    public string MonsterId = Guid.NewGuid().ToString();
    public string Name;
    public int Level;
    public int CurrentHp;
    public int MaxHp;
    public float MagicResistance = 0.15f;
    public bool HasInnateSpells = false;
    public bool IsCharmed = false;
    public string MasterCharacterId = null;
}

public partial class CombatManager : Node
{
    public static CombatManager Instance { get; private set; }

    [Export] public bool IsPaused { get; private set; } = false;

    public override void _Ready()
    {
        Instance = this;
    }

    public override void _UnhandledInput(InputEvent @event)
    {
        if (@event.IsActionPressed("toggle_combat_pause") || 
           (@event is InputEventKey keyEvent && keyEvent.Pressed && keyEvent.Keycode == Key.Space))
        {
            TogglePause();
        }
    }

    public void TogglePause()
    {
        IsPaused = !IsPaused;
        GD.Print($"[CombatManager] Simulation state: {(IsPaused ? "PAUSED" : "RUNNING")}");
    }

    public bool ResolveCharmAttempt(CharacterData caster, MonsterEntity monster)
    {
        float casterPower = (caster.BaseAttributes.Charisma * 2.0f) + caster.Guilds[caster.ActiveGuild].Level;
        float monsterDefense = (monster.Level * 3.0f) * (1.0f + monster.MagicResistance);
        float threshold = Mathf.Clamp(casterPower / monsterDefense, 0.05f, 0.90f);

        float roll = GD.Randf();
        if (roll <= threshold)
        {
            monster.IsCharmed = true;
            monster.MasterCharacterId = caster.CharacterId;
            caster.ActiveCharmedMonster = monster;
            GD.Print($"[Combat] {caster.Callsign} successfully charmed {monster.Name}!");
            return true;
        }

        GD.Print($"[Combat] Charm attempt failed. {monster.Name} enters enraged stance.");
        return false;
    }

    public long SellCharmedMonsterInTown(MonsterEntity monster)
    {
        if (!monster.IsCharmed) return 0;

        long bounty = (monster.Level * 250) + (monster.MaxHp * 15);
        if (monster.HasInnateSpells)
            bounty += 2500;

        GD.Print($"[MonsterMarket] Sold {monster.Name} for {bounty} Gold.");
        return bounty;
    }
}
