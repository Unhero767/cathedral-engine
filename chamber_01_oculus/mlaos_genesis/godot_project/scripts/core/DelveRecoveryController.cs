using Godot;
using System;
using System.Collections.Generic;

public partial class DelveRecoveryController : Node
{
    public static DelveRecoveryController Instance { get; private set; }

    public override void _Ready()
    {
        Instance = this;
    }

    public long CalculateGuildRescueCost(int floor, int charLevel, bool hasHazardModifier)
    {
        long baseFee = 5000;
        long floorPenalty = (long)Math.Pow(floor * 450, 1.85);
        long levelPenalty = charLevel * 1200;
        long total = baseFee + floorPenalty + levelPenalty;

        if (hasHazardModifier)
            total = (long)(total * 1.5);

        return total;
    }

    public bool AttemptResurrection(CharacterData target, int healerGuildLevel)
    {
        target.ResurrectionAttempts++;
        int roll = GD.RandRange(1, 100);
        int successThreshold = (target.BaseAttributes.Constitution * 4) + (healerGuildLevel / 2);

        if (roll <= successThreshold)
        {
            target.MortalityState = "ALIVE";
            target.Status = CharacterStatus.SanctumRest;
            target.CurrentHp = 1;
            target.CurrentAgeYears += 1.5f;
            GD.Print($"[Resurrection] Successful for {target.Callsign}. Age increased to {target.CurrentAgeYears:F1}");
            return true;
        }
        else
        {
            target.BaseAttributes.Constitution = Math.Max(1, target.BaseAttributes.Constitution - 1);
            if (target.ResurrectionAttempts >= 3)
            {
                target.MortalityState = "ASH_FOSSIL";
                target.Status = CharacterStatus.Carbonized;
                GD.PrintErr($"[Resurrection] Critical failure. {target.Callsign} permineralized into ash.");
            }
            return false;
        }
    }
}
