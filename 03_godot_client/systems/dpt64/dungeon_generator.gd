class_name DungeonGenerator
extends RefCounted

const GRID_SIZE = 64

static func generate_strata(seed_val: int) -> Array:
    var rng = RandomNumberGenerator.new()
    rng.seed = seed_val
    
    var grid = []
    for x in range(GRID_SIZE):
        var row = []
        for y in range(GRID_SIZE):
            if x == 0 or y == 0 or x == GRID_SIZE - 1 or y == GRID_SIZE - 1:
                row.append(DPT64Types.CellType.WALL)
            else:
                var val = rng.randf()
                if val < 0.2:
                    row.append(DPT64Types.CellType.WALL)
                elif val < 0.23:
                    row.append(DPT64Types.CellType.TRAP)
                else:
                    row.append(DPT64Types.CellType.EMPTY)
        grid.append(row)
        
    grid[32][32] = DPT64Types.CellType.EMPTY
    grid[2][2] = DPT64Types.CellType.STAIRS_DOWN
    return grid
