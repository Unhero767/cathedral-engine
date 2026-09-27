using Godot;
using System;
using System.Collections.Generic;

[Flags]
public enum TileHazardFlags : uint
{
    None           = 0,
    PitTrap        = 1 << 0,
    Quicksand      = 1 << 1,
    Teleporter     = 1 << 2,
    Spinner        = 1 << 3,
    Submerged      = 1 << 4,
    AntiMagic      = 1 << 5,
    DarknessZone   = 1 << 6,
    PoisonVent     = 1 << 7
}

public class DungeonTile
{
    public int Floor;
    public int X;
    public int Y;
    public TileHazardFlags Hazards = TileHazardFlags.None;
    public Vector3I? TeleportDestination = null;
    public int DropFloorDestination = 0;
}

public partial class DungeonGrid : Node
{
    public const int MaxFloors = 45;
    public const int GridWidth = 32;
    public const int GridHeight = 32;

    public Dictionary<int, DungeonTile[,]> Floors = new();

    public override void _Ready()
    {
        InitializeDungeonFloors();
    }

    private void InitializeDungeonFloors()
    {
        for (int f = 1; f <= MaxFloors; f++)
        {
            DungeonTile[,] floorGrid = new DungeonTile[GridWidth, GridHeight];
            for (int x = 0; x < GridWidth; x++)
            {
                for (int y = 0; y < GridHeight; y++)
                {
                    floorGrid[x, y] = new DungeonTile
                    {
                        Floor = f,
                        X = x,
                        Y = y
                    };

                    // Hazard distribution based on floor brackets
                    if (f >= 11 && f <= 20 && (x + y) % 7 == 0)
                        floorGrid[x, y].Hazards |= TileHazardFlags.Submerged;

                    if (f >= 21 && f <= 30 && (x * y) % 11 == 0)
                        floorGrid[x, y].Hazards |= TileHazardFlags.Quicksand;

                    if (f >= 31 && (x + y) % 9 == 0)
                        floorGrid[x, y].Hazards |= TileHazardFlags.AntiMagic;
                }
            }
            Floors[f] = floorGrid;
        }
        GD.Print($"[DungeonGrid] Initialized {MaxFloors} floors (32x32 deterministic grid).");
    }
}
