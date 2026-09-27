using Godot;
using System;
using System.Collections.Generic;

public enum CharacterStatus
{
    SanctumRest,
    ActiveDelve,
    PinnedInChamber,
    CriticalStasis,
    Carbonized
}

public partial class StableManager : Node
{
    public static StableManager Instance { get; private set; }

    [Export] public int MaxActivePartySize = 4;
    public Dictionary<string, CharacterData> Roster = new();
    public List<string> ActivePartyIds = new();

    public override void _Ready()
    {
        Instance = this;
    }

    public bool DeployParty(List<string> selectedIds, string entranceChamberId)
    {
        if (selectedIds.Count == 0 || selectedIds.Count > MaxActivePartySize)
            return false;

        foreach (var id in selectedIds)
        {
            if (!Roster.ContainsKey(id) || Roster[id].Status != CharacterStatus.SanctumRest)
                return false;
        }

        ActivePartyIds.Clear();
        foreach (var id in selectedIds)
        {
            ActivePartyIds.Add(id);
            Roster[id].Status = CharacterStatus.ActiveDelve;
            Roster[id].CurrentChamberId = entranceChamberId;
        }

        GD.Print($"[StableManager] Deployed active party of {ActivePartyIds.Count} adventurers to {entranceChamberId}");
        return true;
    }

    public void HandlePartyWipe(string chamberId)
    {
        foreach (var id in ActivePartyIds)
        {
            if (Roster.ContainsKey(id))
            {
                Roster[id].Status = CharacterStatus.PinnedInChamber;
                Roster[id].CurrentChamberId = chamberId;
                Roster[id].MortalityState = "DEAD_IN_DUNGEON";
            }
        }

        ActivePartyIds.Clear();
        GD.PrintErr($"[StableManager] Active squad pinned at chamber {chamberId}. Emergency rescue protocol activated.");
    }
}
