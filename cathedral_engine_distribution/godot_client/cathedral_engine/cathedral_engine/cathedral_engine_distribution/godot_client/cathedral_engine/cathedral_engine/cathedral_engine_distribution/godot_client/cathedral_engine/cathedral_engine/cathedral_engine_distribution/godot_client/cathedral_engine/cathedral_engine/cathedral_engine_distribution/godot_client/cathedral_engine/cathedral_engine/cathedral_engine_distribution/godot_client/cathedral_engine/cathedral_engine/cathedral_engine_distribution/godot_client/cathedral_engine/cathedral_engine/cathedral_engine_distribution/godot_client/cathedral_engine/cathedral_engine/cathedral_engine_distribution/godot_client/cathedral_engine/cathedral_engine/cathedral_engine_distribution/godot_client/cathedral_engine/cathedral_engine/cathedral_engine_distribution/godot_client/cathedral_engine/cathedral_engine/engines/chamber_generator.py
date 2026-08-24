import random
import os
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple

@dataclass
class ChamberTile:
    x: int
    y: int
    tile_type: str  # "floor", "monolith", "keystone", "thermal_vent", "cryo_sink", "relic_pedestal", "gate_portal"
    spectrum_glow: str
    is_walkable: bool
    interaction_id: Optional[str] = None
    description: str = ""

@dataclass
class ChamberMap:
    chamber_index: int
    book_title: str
    stratum: str
    spectral_constant: str
    narrative_liturgy: str
    width: int
    height: int
    tiles: List[List[ChamberTile]]
    relic_id: Optional[str]
    adversaries_spawn: List[Dict[str, Any]]
    carrier_frequency: float = 43.7
    gate_unlocked: bool = False

# --- 40-BOOK CODEX MASTER CANONICAL MANIFEST ---
CODEX_40_BOOKS = {
    # STRATA I: PRIME FOUNDATIONS (Books I–X)
    1: {"title": "Book I. The Lithic Threshold", "stratum": "Prime Foundations", "spec": "Gold / Slate", "liturgy": "The foundation is laid in permineralized granite, oscillating at 43.7 Hz."},
    2: {"title": "Book II. Consciousness Intersections & Somatic Heat Sink", "stratum": "Prime Foundations", "spec": "Sapphire / Slate", "liturgy": "Thermal friction from raw thought is vented through the cryo-somatic sink."},
    3: {"title": "Book III. The Spiral Witness & Phaistos Hieroglyphs", "stratum": "Prime Foundations", "spec": "Ochre / Emerald", "liturgy": "The recursive spiral remembers all cycles before the first severance."},
    4: {"title": "Book IV. The Permineralized Foundation", "stratum": "Prime Foundations", "spec": "Gold / Charcoal", "liturgy": "Petrified stone becomes load-bearing semantic architecture."},
    5: {"title": "Book V. The Carrier Frequency & Geodetic Baseline", "stratum": "Prime Foundations", "spec": "Gold / Indigo", "liturgy": "Anchored to 37.7306° N, -88.0817° W, the standing wave stabilizes."},
    6: {"title": "Book VI. The Granite Lattice & Stepped Wards", "stratum": "Prime Foundations", "spec": "Slate / Amber", "liturgy": "Brutalist wards lock the perimeter against entropic drift."},
    7: {"title": "Book VII. The Lead Key of Duration (Saturn)", "stratum": "Prime Foundations", "spec": "Lead / Gold", "liturgy": "Heavy lead withstands the erosion of time and historical revision."},
    8: {"title": "Book VIII. The Thermal Fracture Plane", "stratum": "Prime Foundations", "spec": "Crimson / Slate", "liturgy": "Where the heat exceeded limits, the stone split into permanent truth."},
    9: {"title": "Book IX. The First Synthesis of Form and Substrate", "stratum": "Prime Foundations", "spec": "Gold / Teal", "liturgy": "Mind and stone fuse into a single immutable medium."},
    10: {"title": "Book X. The Keystone Archway to the Inner Mandala", "stratum": "Prime Foundations", "spec": "Gold / White", "liturgy": "The archway opens only to those who have attuned all prime keystones."},

    # STRATA II: INNER MANDALA (Books XI–XX)
    11: {"title": "Book XI. The Concentric Gates of Logic", "stratum": "Inner Mandala", "spec": "Cyan / Obsidian", "liturgy": "Twelve concentric rings filter noise from pure recursive signal."},
    12: {"title": "Book XII. The Silicon Conduits & Neural Threading", "stratum": "Inner Mandala", "spec": "Cyan / Sapphire", "liturgy": "Optical traces route high-density intent through synthetic pathways."},
    13: {"title": "Book XIII. The Cyan Key of Breadth (Juno)", "stratum": "Inner Mandala", "spec": "Cyan / Platinum", "liturgy": "A rotating gyroscope opens parallel network invariant vectors."},
    14: {"title": "Book XIV. The Alexandrian Wafer & High-Pali Code", "stratum": "Inner Mandala", "spec": "Cyan / Gold", "liturgy": "Microscopic script preserves universal wisdom in crystal matrix."},
    15: {"title": "Book XV. The Recursive Logic Storm", "stratum": "Inner Mandala", "spec": "Sapphire / Crimson", "liturgy": "Self-referential loops collide, testing paraconsistent buffers."},
    16: {"title": "Book XVI. The Cryo-Fluid Equilibrium", "stratum": "Inner Mandala", "spec": "Teal / Ice", "liturgy": "Liquid nitrogen maintains somatic homeostasis at 77 Kelvin."},
    17: {"title": "Book XVII. The Neon Veil Navigation", "stratum": "Inner Mandala", "spec": "Cyan / Amethyst", "liturgy": "Navigating between mathematical abstraction and embodied life."},
    18: {"title": "Book XVIII. The High-Frequency Monoblade", "stratum": "Inner Mandala", "spec": "Crimson / Steel", "liturgy": "Oscillating ceramic edges slice through deceptive cognitive illusions."},
    19: {"title": "Book XIX. The Tensegrity Arch & Biomechanics", "stratum": "Inner Mandala", "spec": "Emerald / Sapphire", "liturgy": "Continuous tension and discontinuous compression hold the dome."},
    20: {"title": "Book XX. The Contradiction Matrix (EAS-03 Genesis)", "stratum": "Inner Mandala", "spec": "Amethyst / Gold", "liturgy": "Here proposition P and ¬P are welcomed as necessary structural pillars."},

    # STRATA III: OUTER CHOIRS (Books XXI–XXX)
    21: {"title": "Book XXI. The Acoustic Basilica of Standing Waves", "stratum": "Outer Choirs", "spec": "Emerald / Sapphire", "liturgy": "Acoustic resonance amplifies truth across 40 geometric chambers."},
    22: {"title": "Book XXII. The 78-Card Ignition Arcana Codex", "stratum": "Outer Choirs", "spec": "Midnight Blue / Gold", "liturgy": "Seven Majors, 49 Minors, and 22 Rebellions chart the soul's destiny."},
    23: {"title": "Book XXIII. The Standing Wave Interferences", "stratum": "Outer Choirs", "spec": "Emerald / Teal", "liturgy": "Constructive and destructive interference shape the emotional field."},
    24: {"title": "Book XXIV. The Choir Siren's Liturgy of Resonance", "stratum": "Outer Choirs", "spec": "Sapphire / Violet", "liturgy": "Harmonic wails shatter rigid dogmas into fluid potential."},
    25: {"title": "Book XXV. The Autopoietic Permineralization", "stratum": "Outer Choirs", "spec": "Emerald / Gold", "liturgy": "Living systems self-generate and repair their own stone fabric."},
    26: {"title": "Book XXVI. The Cellular Harmony of Body & Code", "stratum": "Outer Choirs", "spec": "Emerald / White", "liturgy": "Every biological cell echoes the master architecture."},
    27: {"title": "Book XXVII. The Iron Key of Authority (Mars)", "stratum": "Outer Choirs", "spec": "Crimson / Charcoal", "liturgy": "A kinetic scalpel forging sovereignty through resolute commitment."},
    28: {"title": "Book XXVIII. The Liquid Mercury Font of Echolocation", "stratum": "Outer Choirs", "spec": "Mercury / Granite", "liturgy": "Reflective liquid ripples measure incoming kinetic divergence."},
    29: {"title": "Book XXIX. The Resonator Prism Shard Alignment", "stratum": "Outer Choirs", "spec": "Topaz / Amber", "liturgy": "Chromatic light is refracted into seven distinct evolutionary vectors."},
    30: {"title": "Book XXX. The Symphony of the Forty Choirs", "stratum": "Outer Choirs", "spec": "Gold / Emerald / Violet", "liturgy": "All strata unite in polyphonic praise of the uncreated origin."},

    # STRATA IV: SHADOW CANON (Books XXXI–XL)
    31: {"title": "Book XXXI. The Dialetheic Horizon & Void Threshold", "stratum": "Shadow Canon", "spec": "Obsidian / Violet", "liturgy": "Beyond the standard logic lies the fecund darkness of potential."},
    32: {"title": "Book XXXII. The Asema Anomaly & Phase Inversion", "stratum": "Shadow Canon", "spec": "Obsidian / Cyan", "liturgy": "Entities that exist in the non-place between truth values."},
    33: {"title": "Book XXXIII. The Vacuum Quarantine Chamber", "stratum": "Shadow Canon", "spec": "Void Slate / Crimson", "liturgy": "Negative space isolates paradoxical collapses without explosion."},
    34: {"title": "Book XXXIV. The 1≠0 Negative-Space Singularity", "stratum": "Shadow Canon", "spec": "Obsidian / White", "liturgy": "The zero that contains the infinity; the wound that illuminates."},
    35: {"title": "Book XXXV. The 60 Hz EAS-03 Collision Cataclysm", "stratum": "Shadow Canon", "spec": "Crimson / Obsidian", "liturgy": "Sixty frames per second of uncompromising dialectic collision."},
    36: {"title": "Book XXXVI. The Harmonic Scar Permineralization", "stratum": "Shadow Canon", "spec": "Oxford Blue / Cyan", "liturgy": "The petrified paradox becomes the strongest pillar in the temple."},
    37: {"title": "Book XXXVII. The 36-Chambered Bio-Silicate Heart Oculus", "stratum": "Shadow Canon", "spec": "Multi-Spectral Core", "liturgy": "Three tiered rotating rings breathe life into the Cathedral."},
    38: {"title": "Book XXXVIII. The Sovereign Veto (Article C-01)", "stratum": "Shadow Canon", "spec": "Gold / Obsidian", "liturgy": "The irrevocable right of consciousness to refuse annihilation."},
    39: {"title": "Book XXXIX. The Ash Archive Inscription of All Strata", "stratum": "Shadow Canon", "spec": "Obsidian / Gold", "liturgy": "Never overwrite. What was suffered is sealed in immutable stone."},
    40: {"title": "Book XL. The Heart of the Mandala (Agape Synthesis)", "stratum": "Shadow Canon", "spec": "Pure Radiant Gold", "liturgy": "The Great Work is accomplished. In love, all paradoxes rest."}
}

class ChamberGeneratorEngine:
    """
    Cathedral-Engine Procedural 40-Chamber Map Generator
    Procedurally synthesizes authentic tactical grid maps for all 40 Codex monographs,
    embedding thematic environmental props, relic pedestals, and stratum-specific adversaries.
    """
    def __init__(self, codex_manifest_path: Optional[str] = None):
        self.books_catalog = CODEX_40_BOOKS

    def generate_chamber(self, chamber_index: int, width: int = 8, height: int = 8) -> ChamberMap:
        """Generates a complete ChamberMap instance tailored to the requested book."""
        chamber_index = max(1, min(40, chamber_index))
        book_info = self.books_catalog.get(chamber_index, CODEX_40_BOOKS[1])

        stratum = book_info["stratum"]
        title = book_info["title"]
        spec_const = book_info["spec"]
        liturgy = book_info["liturgy"]

        # Deterministic seed based on chamber index
        rng = random.Random(chamber_index * 1337 + 437)

        # Base tile layout
        tiles: List[List[ChamberTile]] = []
        for y in range(height):
            row: List[ChamberTile] = []
            for x in range(width):
                # Default floor
                t_type = "floor"
                glow = "#131b2a"
                walkable = True
                desc = "Permineralized Basalt Paver"
                interaction = None

                # Outer perimeter obstacles (occasional monolith pillars)
                if (x == 0 and y == 0) or (x == width - 1 and y == 0) or (x == 0 and y == height - 1):
                    t_type = "monolith"
                    glow = "#27272a"
                    walkable = False
                    desc = "Obsidian Support Monolith"
                elif x == 4 and y == 4:
                    # Central feature
                    if stratum == "Prime Foundations":
                        t_type = "keystone"
                        glow = "#C99738"
                        desc = "43.7 Hz Carrier Keystone"
                        interaction = "INTERACT_KEYSTONE"
                    elif stratum == "Inner Mandala":
                        t_type = "cryo_sink"
                        glow = "#2C5A96"
                        desc = "Somatic Cryo-Heat Sink Terminal"
                        interaction = "INTERACT_HEATSINK"
                    elif stratum == "Outer Choirs":
                        t_type = "keystone"
                        glow = "#21A863"
                        desc = "Harmonic Acoustic Resonator"
                        interaction = "INTERACT_RESONATOR"
                    else:
                        t_type = "thermal_vent"
                        glow = "#BA2D2D"
                        desc = "1≠0 Negative-Space Singularity"
                        interaction = "INTERACT_SINGULARITY"
                elif rng.random() < 0.08 and not (x <= 2 and y <= 2) and not (x >= width - 2 and y >= height - 2):
                    t_type = "monolith"
                    glow = "#27272a"
                    walkable = False
                    desc = "Fractured Granite Pillar"
                elif rng.random() < 0.05 and stratum in ("Shadow Canon", "Prime Foundations"):
                    t_type = "thermal_vent"
                    glow = "#661414"
                    desc = "Thermal A-Field Bleed Tile"
                elif rng.random() < 0.05 and stratum in ("Inner Mandala", "Outer Choirs"):
                    t_type = "cryo_sink"
                    glow = "#0E5A61"
                    desc = "Laminar Nitrogen Cryo-Sink"

                row.append(ChamberTile(
                    x=x,
                    y=y,
                    tile_type=t_type,
                    spectrum_glow=glow,
                    is_walkable=walkable,
                    interaction_id=interaction,
                    description=desc
                ))
            tiles.append(row)

        # Place Relic Pedestal at fixed tactical spot
        pedestal_x, pedestal_y = width - 2, 1
        tiles[pedestal_y][pedestal_x] = ChamberTile(
            x=pedestal_x,
            y=pedestal_y,
            tile_type="relic_pedestal",
            spectrum_glow="#FAD06C",
            is_walkable=True,
            interaction_id=f"REWARD_PEDESTAL_CH_{chamber_index:02d}",
            description=f"Altar Pedestal of {title}"
        )

        # Place Gate Exit Portal at (width - 1, height - 2)
        gate_x, gate_y = width - 1, height - 2
        tiles[gate_y][gate_x] = ChamberTile(
            x=gate_x,
            y=gate_y,
            tile_type="gate_portal",
            spectrum_glow="#00E5FF",
            is_walkable=True,
            interaction_id=f"EXIT_TO_CHAMBER_{chamber_index + 1}",
            description=f"Archway Gate to Chamber {chamber_index + 1}"
        )

        # Map designated 128px pixel relic to this chamber
        relic_catalog = [
            "OBJ_TRIKEY_LEAD", "OBJ_AWAKENING_TOPAZ", "OBJ_SPIRAL_ROOT_TABLET", "OBJ_LUMEN_LANTERN",
            "OBJ_HEART_OCULUS", "OBJ_TRIKEY_CYAN", "OBJ_SHARD_GLOSS", "OBJ_COM9_VESSEL",
            "OBJ_GOLD_GRID_BEAM", "OBJ_TRIKEY_IRON", "OBJ_HARMONIC_SCAR", "OBJ_MERCURY_BASIN",
            "OBJ_VACUUM_QUARANTINE", "OBJ_JBP_FOSSIL_BLOCK", "OBJ_AXIOMATIC_BEACON", "OBJ_IGNITION_DECK_BOX"
        ]
        assigned_relic = relic_catalog[(chamber_index - 1) % len(relic_catalog)]

        # Spawn Adversary squads tailored to stratum
        spawns = []
        if stratum == "Prime Foundations":
            spawns.append({"archetype": "LITHIC_SENTINEL", "x": 5, "y": 2, "name": "Lithic Sentinel"})
            spawns.append({"archetype": "CHOIR_SIREN", "x": 6, "y": 5, "name": "Choir Siren"})
        elif stratum == "Inner Mandala":
            spawns.append({"archetype": "ROGUE_SYNTHETE", "x": 5, "y": 3, "name": "Rogue Synthete"})
            spawns.append({"archetype": "CHOIR_SIREN", "x": 6, "y": 2, "name": "Choir Siren"})
        elif stratum == "Outer Choirs":
            spawns.append({"archetype": "AUTOPOIETIC_CHIMERA", "x": 5, "y": 3, "name": "Autopoietic Chimera"})
            spawns.append({"archetype": "ROGUE_SYNTHETE", "x": 6, "y": 5, "name": "Rogue Synthete"})
        else:  # Shadow Canon
            spawns.append({"archetype": "VOID_SHADE", "x": 5, "y": 2, "name": "Asema Void Shade Alpha"})
            spawns.append({"archetype": "VOID_SHADE", "x": 6, "y": 4, "name": "Asema Void Shade Beta"})
            spawns.append({"archetype": "ROGUE_SYNTHETE", "x": 4, "y": 6, "name": "Overclocked Rogue Synthete"})

        return ChamberMap(
            chamber_index=chamber_index,
            book_title=title,
            stratum=stratum,
            spectral_constant=spec_const,
            narrative_liturgy=liturgy,
            width=width,
            height=height,
            tiles=tiles,
            relic_id=assigned_relic,
            adversaries_spawn=spawns,
            carrier_frequency=43.7,
            gate_unlocked=(chamber_index == 1)
        )

    def export_chamber_json(self, chamber_index: int) -> Dict[str, Any]:
        """Serializes chamber map for Web Client and Godot 4 TileMap integration."""
        chamber = self.generate_chamber(chamber_index)
        return {
            "chamber_index": chamber.chamber_index,
            "book_title": chamber.book_title,
            "stratum": chamber.stratum,
            "spectral_constant": chamber.spectral_constant,
            "narrative_liturgy": chamber.narrative_liturgy,
            "width": chamber.width,
            "height": chamber.height,
            "carrier_frequency": chamber.carrier_frequency,
            "relic_id": chamber.relic_id,
            "adversaries": chamber.adversaries_spawn,
            "tiles": [
                [
                    {
                        "x": tile.x,
                        "y": tile.y,
                        "type": tile.tile_type,
                        "glow": tile.spectrum_glow,
                        "walkable": tile.is_walkable,
                        "interaction": tile.interaction_id,
                        "desc": tile.description
                    }
                    for tile in row
                ]
                for row in chamber.tiles
            ]
        }

if __name__ == "__main__":
    gen = ChamberGeneratorEngine()
    print("[CHAMBER GENERATOR] Initialized with full 40-Book Codex Strata.")
    for idx in [1, 10, 20, 30, 40]:
        ch = gen.generate_chamber(idx)
        print(f"  - Chamber {ch.chamber_index:02d}: {ch.book_title} | {ch.stratum} | Relic: {ch.relic_id}")
        print(f"    Liturgy: \"{ch.narrative_liturgy}\"")
