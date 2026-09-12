"""
Asset 2: Cathedral-Engine Combat Loop State Machine.
Handles turn sequencing, A-Field thermal dynamics, Vault I-V tile mechanics,
and Shader color ratio mapping for WebGL rendering payloads.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Tuple, Optional, Any

class TileType(str, Enum):
    NORMAL = "NORMAL"
    LITHIC_MONOLITH = "LITHIC_MONOLITH"
    RESONANCE_KEYSTONE = "RESONANCE_KEYSTONE"
    A_FIELD_THERMAL = "A_FIELD_THERMAL"
    BLUE_SORROW_SINK = "BLUE_SORROW_SINK"
    ASYMPTOTIC_CORRIDOR = "ASYMPTOTIC_CORRIDOR"
    DIALETHEIC_SINGULARITY = "DIALETHEIC_SINGULARITY"

class SpectrumAffinity(str, Enum):
    GOLD = "GOLD"
    TEAL = "TEAL"
    BLUE = "BLUE"
    RED = "RED"
    VIOLET = "VIOLET"
    EMERALD = "EMERALD"
    BRONZE_OBSIDIAN = "BRONZE_OBSIDIAN"

@dataclass
class GridTile:
    x: int
    y: int
    tile_type: TileType = TileType.NORMAL
    spectrum: SpectrumAffinity = SpectrumAffinity.TEAL
    heat_level: float = 0.0
    paradox_charge: float = 0.0
    is_walkable: bool = True

@dataclass
class RPGCharacter:
    name: str
    max_hp: int
    current_hp: int
    x: int = 0
    y: int = 0
    action_points: int = 4
    max_ap: int = 4
    a_field_temp_k: float = 300.0

class CombatLoopEngine:
    def __init__(self, character: RPGCharacter, width: int = 8, height: int = 8):
        self.character = character
        self.width = width
        self.height = height
        self.grid = self._init_grid()

    def _init_grid(self) -> List[List[GridTile]]:
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile_type = TileType.NORMAL
                spec = SpectrumAffinity.TEAL
                if (x, y) == (2, 2): tile_type, spec = TileType.LITHIC_MONOLITH, SpectrumAffinity.BRONZE_OBSIDIAN
                elif (x, y) == (4, 4): tile_type, spec = TileType.RESONANCE_KEYSTONE, SpectrumAffinity.GOLD
                elif (x, y) == (1, 3): tile_type, spec = TileType.A_FIELD_THERMAL, SpectrumAffinity.RED
                elif (x, y) == (5, 2): tile_type, spec = TileType.BLUE_SORROW_SINK, SpectrumAffinity.BLUE
                elif (x, y) == (6, 6): tile_type, spec = TileType.DIALETHEIC_SINGULARITY, SpectrumAffinity.BRONZE_OBSIDIAN

                row.append(GridTile(x=x, y=y, tile_type=tile_type, spectrum=spec, is_walkable=(tile_type != TileType.LITHIC_MONOLITH)))
            grid.append(row)
        return grid

    def move_character(self, target_x: int, target_y: int) -> Tuple[bool, str]:
        if not (0 <= target_x < self.width and 0 <= target_y < self.height):
            return False, "Target out of bounds."

        tile = self.grid[target_y][target_x]
        if not tile.is_walkable:
            return False, "Movement blocked by Lithic Monolith."

        self.character.x, self.character.y = target_x, target_y
        log = f"Moved to ({target_x}, {target_y})."

        if tile.tile_type == TileType.A_FIELD_THERMAL:
            self.character.a_field_temp_k += 25.0
            log += " Thermal tile stepped (+25K)."
        elif tile.tile_type == TileType.BLUE_SORROW_SINK:
            self.character.a_field_temp_k = max(300.0, self.character.a_field_temp_k - 30.0)
            log += " Heat sink stepped (-30K)."

        return True, log
