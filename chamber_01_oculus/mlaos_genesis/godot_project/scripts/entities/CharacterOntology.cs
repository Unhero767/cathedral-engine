using Godot;
using System;
using System.Collections.Generic;

public enum RaceType
{
    Human,
    Elf,
    Dwarf,
    Gnome,
    Giant,
    Ogre,
    Morloch,
    Osiri,
    Troll
}

public enum AlignmentType
{
    Good,
    Neutral,
    Evil
}

public enum GuildType
{
    Nomad,
    Warrior,
    Paladin,
    Ninja,
    Villain,
    Seeker,
    Thief,
    Scavenger,
    Mage,
    Sorcerer,
    Wizard,
    Healer
}

public class Attributes
{
    public int Strength;
    public int Intelligence;
    public int Wisdom;
    public int Constitution;
    public int Charisma;
    public int Dexterity;
}

public class GuildProgress
{
    public GuildType Guild;
    public int Level = 1;
    public long CurrentXp = 0;
    public bool QuestCompleted = true;
}

public class CharacterData
{
    public string CharacterId = Guid.NewGuid().ToString();
    public string Callsign;
    public RaceType Race;
    public AlignmentType Alignment;
    public CharacterStatus Status = CharacterStatus.SanctumRest;
    public string MortalityState = "ALIVE";

    public Attributes BaseAttributes = new();
    public Attributes NaturalCaps = new();

    public GuildType ActiveGuild = GuildType.Nomad;
    public Dictionary<GuildType, GuildProgress> Guilds = new();

    public int CurrentHp = 20;
    public int MaxHp = 20;
    public float CurrentAgeYears = 18.0f;
    public int MaxNaturalAge = 80;
    public int ResurrectionAttempts = 0;

    public string CurrentChamberId = "SANCTUM";
    public MonsterEntity ActiveCharmedMonster = null;

    public CharacterData()
    {
        Guilds[GuildType.Nomad] = new GuildProgress { Guild = GuildType.Nomad, Level = 1 };
    }

    public int GetHighestGuildLevel()
    {
        int highest = 0;
        foreach (var entry in Guilds.Values)
        {
            if (entry.Level > highest)
                highest = entry.Level;
        }
        return highest;
    }

    public long CalculateNextLevelXp(GuildType targetGuild)
    {
        int currentLvl = Guilds.ContainsKey(targetGuild) ? Guilds[targetGuild].Level : 1;
        long baseCost = (long)(Math.Pow(currentLvl, 2.1) * 100);
        int multiClassCount = Math.Max(0, Guilds.Count - 1);
        double penaltyMultiplier = Math.Pow(1.35, multiClassCount);
        return (long)(baseCost * penaltyMultiplier);
    }
}
