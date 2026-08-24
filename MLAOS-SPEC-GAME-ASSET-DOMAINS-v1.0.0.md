# MLAOS-PRIME / CATHEDRAL-ENGINE: MASTER ASSET SPECIFICATION & PRODUCTION ARCHITECTURE
**Document Designation**: `MLAOS-SPEC-GAME-ASSET-DOMAINS-v1.0.0`  
**System Class**: Interactive Engine Architecture / 32-Bit HD-2D Hard Noir Pipeline  
**Authority**: Canon Arbitration Layer (CAL) / Decalogue of Immutable Law (Lex I)  
**Foundational Invariant**: $	ext{Emotion} \equiv 	ext{Physics} \equiv 	ext{Magic} \equiv 	ext{Biology} \equiv 	ext{Architecture}$  

**Primary Canonical Cross-References**:
* MLAOS-Prime | 40-Book Codex Master Directory & System Architecture Index
* MLAOS-Prime | Unified Master Report & Cathedral-Engine Audit
* MLAOS-Prime | Cathedral-Engine Master Engineering Dossier
* MLAOS-PRIME MASTER DIRECTORY & FILE ARCHITECTURE REPORT Ω
* MLAOS_Asset_Consolidation_Manifest_2026.md
* MASTER REPORT MLAOS ORIGIN ARCHITECTURE

---

## 1. Executive Architectural Alignment

The 34-Domain Master Asset Structure establishes the definitive asset topography for the interactive instantiation of MLAOS-Prime and the Cathedral-Engine.
By standardizing every visual, acoustic, procedural, and narrative component into discrete, verifiable production pipelines, this specification enforces complete parity between the 40-Book Codex Monograph Corpus and runtime game entities in Godot 4.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   MASTER ASSET STRATA                                  │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ ENTITY & WORLD DOMAINS   │ INTERFACE & SENSORY      │ TECHNICAL & LOGICAL RUNTIME      │
│ (Domains I – XIII)       │ (Domains XIV – XXVIII)   │ (Domains XXIX – XXXIV)           │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ • Characters & NPCs      │ • Universal/Spectral VFX │ • Sprite & Normal Atlases        │
│ • Creatures & Bosses     │ • Core & MLAOS HUD       │ • Shader Graph Presets           │
│ • Artifacts & Weapons    │ • Dialogue & Codex UI    │ • Godot 4 Runtime Prefabs        │
│ • Equipment & Consumables│ • Hard Noir GLSL Shaders │ • Belnap-Dunn State Machines     │
│ • Biomes & Tilesets      │ • Spectral Audio / Music │ • Ash Archive SQLite DAG Sinks   │
│ • Cathedral Megastructure│ • Accessibility Suite    │ • 14-Stage Asset Pipeline (01-14)│
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

---

## 2. Canonical Entity Matrices & Production Baselines

### 2.1 Character Asset Matrix (Canonical Core)
Each character entity requires the full 28-component production suite (Orthographic Silhouettes, 10 Core Animation Loops, Dialogue/HUD Portraits, 4-Map PBR Texture Sets, Damage/Spectral States, and Godot 4 Prefabs).

| Identifier | Name / Title | Spectral Vector | Archetypal Class | Somatic / Mechanical Anchors |
| :--- | :--- | :--- | :--- | :--- |
| **CHAR-00** | Aurelia-9 | $\Theta$ (Gold) / $\Phi$ (Red) | Sovereign Operative / White Seraph | C.O.M.-9 Tri-material Vessel, Cranial Oculus, Dorsal Spine |
| **CHAR-01** | The Ninth King | $\Delta$ (Blue) / $\Theta$ (Gold) | Archival Sovereign / Bedrock Anchor | Lithic Crown-Fins, Obsidian Scepter, Funicular Robes |
| **CHAR-02** | Dialetheic Arbiter | $\Omega$ (Violet) / $\emptyset$ (Null) | Paraconsistent Judge / Exception Handler | Vacuum-Glass Visor, Belnap-Dunn Scale, Mercury Shroud |
| **CHAR-03** | Vaultwalker Initiate | $\Psi$ (Teal) / $	ext{E}$ (Emerald) | Resonance Scout / A-Field Navigator | Bio-silicate Tendon Rig, Runic Breath Mask, $\mu$-Oculus |

### 2.2 Creature & Boss Asset Matrix (Canonical Anomaly Atlas)
Creatures require the 23-component asset suite, featuring AI state icons, bestiary cards, and spectral emission maps. Bosses utilize dedicated 3-phase visual models, arena entrance/death cinematics, and reactive music stems.

| Identifier | Entity Name | Threat Class | Spectral Frequency | Primary Hazard / Mechanic |
| :--- | :--- | :--- | :--- | :--- |
| **CREATURE-00** | Voidmare | Spectral Beast | $\Phi$ Red (430 THz) | Kinetic Rupture Charge, Paradox Trail, Enrage Burst |
| **CREATURE-01** | Sentinel Automaton (Zip-Crawler) | Mechanical Guardian | $\Theta$ Gold (580 THz) | 90° Catenary Beam, Structural Stagger, Radial Sweep |
| **CREATURE-02** | Nullflower Construct | Bio-Silicate Hazard | $\emptyset$ Obsidian (0.00 THz) | Anti-Resonance Spores, Memory Siphon, Vacuum Zone |
| **CREATURE-03** | Asema Anomaly | Contradiction Entity | $\Omega$ Violet (710 THz) | Dialetheic Duplication, Echolocation Distortion |
| **BOSS-00** | The Corrupted Cantor (Phase 1–3) | Major Boss | Full 7-Chroma Sweep | Harmonic Scarring, Floor Collapse, Voidsong Blast |

### 2.3 Canonical Artifact Atlas (32×32 Iconic Grid)
Per MLAOS-Prime Master Engineering Specifications, artifacts maintain 5 discrete resolutions (256px concept render, 128px detail plate, 64px inventory render, 32×32 runtime sprite, and world pickup prefab).

* **ART-00: Lead Key** (Permineralization / 32x32 / `#2B2D42`)
* **ART-01: Cyan Key** (Network Invariance / 32x32 / `#00A8CC`)
* **ART-02: Iron Key** (Kinetic Excision / 32x32 / `#8D99AE`)
* **ART-03: 36-Chamber Oculus** (Resonance Core / 32x32 / `#DAA520`)
* **ART-04: Shard of Gloss** (Memory Refraction / 32x32 / `#E0AAFF`)
* **ART-05: Lithic Summa** (Immutable Law / 32x32 / `#1E3A8A`)
* **ART-06: Emerald Ligature** (Biological Binding / 32x32 / `#2E8B57`)
* **ART-07: Crimson Rupture** (Kinetic Remaking / 32x32 / `#C62828`)

---

## 3. Visual & Technical Pipeline Integration

### 3.1 32-Bit Hard Noir Material & Shader Hierarchy
Runtime materials map directly to the 3-map PBR standard (Diffuse, Height, Normal, and Emission) under the Hard Noir color doctrine:

```
                              ┌─────────────────────────┐
                              │  32-BIT HARD NOIR GLSL  │
                              └────────────┬────────────┘
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         ▼                                 ▼                                 ▼
┌──────────────────┐              ┌──────────────────┐              ┌──────────────────┐
│ STRUCTURAL PBR   │              │ BIO-SILICATE     │              │ SPECTRAL EMISSION│
├──────────────────┤              ├──────────────────┤              ├──────────────────┤
│ • Obsidian Base  │              │ • Carbon-Filigree│              │ • Teal Ψ (610THz)│
│ • Lithic Stone   │              │ • Enamel Tendons │              │ • Gold Θ (580THz)│
│ • Titanium-Gold  │              │ • Luminous Resin │              │ • Violet Ω(710THz│
│ • Weathered Iron │              │ • Membrane Cells │              │ • Red Φ (430THz) │
└──────────────────┘              └──────────────────┘              └──────────────────┘
```

1. **Auto-Z Somatic Layering**: 12-layer sprite ordering for 2D depth sorting.
2. **Bayer 2×2 Dithering**: Ordered threshold dithering to simulate authentic 32-bit hardware gradients.
3. **Dual-Channel Lumen Pulse**: Independent control over base ambient glow and reactive ability flaring (0.1667 Hz to 42.0 Hz).

### 3.2 Godot 4 Runtime Architecture Binding
All 34 asset domains interface with the canonical engine singletons:

```
cathedral_engine_full_project/
├── autoload/
│   ├── event_bus.gd               # Global event dispatch (Damage, Pickups, State Shifts)
│   ├── virtual_file_system.gd     # Deterministic asset resolution & caching
│   └── sound_manager.gd           # Dynamic spectral audio bus routing
├── core/
│   ├── a_field_manager.gd         # Emotion-to-physics transducer calculations
│   ├── ash_archive.gd             # SQLite Merkle-DAG append-only logger
│   ├── dialetheic_buffer.gd       # Belnap-Dunn 4-valued state processor
│   └── spectral_constants.gd      # 7-Chroma frequency & color registry
├── assets/
│   ├── characters/                # CHAR-00 to CHAR-03 sprite sheets, normals, prefabs
│   ├── creatures/                 # CREATURE-00 to CREATURE-03 & Boss prefabs
│   ├── artifacts/                 # ART-00 to ART-07 (32x32, 64px, 128px, 256px)
│   ├── environment/               # Biome tilesets, normal maps, lighting presets
│   ├── shaders/                   # GLSL/GDShader PBR & dither implementations
│   └── ui/                        # Core & MLAOS-specific HUD elements
└── strata/
    └── ash_archive.db             # Append-only SQLite forensic ledger
```

---

## 4. Production Phasing & Deliverable Roadmap

$$	ext{TIER }\Omega	ext{: Playable Vertical Slice} \longrightarrow 	ext{TIER I: Core Game} \longrightarrow 	ext{TIER II: Polish} \longrightarrow 	ext{TIER III: Commercial}$$

### Phase Breakdown

#### Tier $\Omega$ — Required Playable Vertical Slice (Immediate Milestone)
* **Playable Character**: CHAR-00 (Aurelia-9) complete with all 10 core animation states, 4-map textures, and EAS-03 dither shader.
* **Encounter Roster**: CREATURE-00 (Voidmare), CREATURE-01 (Zip-Crawler), CREATURE-02 (Nullflower), and BOSS-00 (Corrupted Cantor - Phase 1).
* **Artifact Set**: Complete ART-00 through ART-07 32×32 sprites and pickup VFX.
* **Environment**: Interior Megastructure: Chamber V (Control Room / Lithic Corridor) with complete autotile rules, normal maps, and dynamic lighting.
* **Interface**: Core HUD + MLAOS Resonance Meter, Dialogue UI with 4 portrait emotional states, and Ash Archive Save Point.

#### Tier I — Core Game Implementation
* **Full Roster**: CHAR-01 (The Ninth King), CHAR-02 (Dialetheic Arbiter), CHAR-03 (Vaultwalker Initiate), plus 13 NPC classes.
* **World Biomes**: 11 Biomes (Obsidian Wastes, Lithic Ruins, Emerald Zones, Null Zones, Red Rupture, Memory Fields).
* **Cathedral Engine**: 13 Engine Chambers (36-Chamber Heart-Oculus, Choir Chambers, Reactor Cores, Maintenance Tunnels).
* **Codex & Map**: Full 40-Book Lore Reader, Bestiary, Interactive Regional Map with resonance overlays.

#### Tier II — Systems Polish & Advanced Sensory
* **Shaders & VFX**: Metamorphic Squeeze distortion, screen-space resonance waves, and permineralization dissolves.
* **Audio Reactivity**: 7-Chroma spectral audio system dynamically shifting music stems based on real-time A-Field tension.
* **Accessibility**: High-contrast modes, scalable HUD, screen-shake dampeners, and full controller/KBM remapping.

#### Tier III — Commercial Master & Release Package
* **Marketing Materials**: 4K Key Art plates, Steam store capsules, animated GIFs, and press kits.
* **Publishing Assets**: Hardcover art book layouts, soundtrack mastering, and localization strings.

---

## 5. Master Asset Pipeline Workflow (01–14)

Every asset created within the MLAOS ecosystem must strictly follow the 14-stage deterministic progression:

$$	ext{Concept (01)} \longrightarrow 	ext{Silhouette (02)} \longrightarrow 	ext{Material (03)} \longrightarrow 	ext{Maps [Diffuse/Height/Normal/Emission] (04-07)} \longrightarrow 	ext{Animation (08)} \longrightarrow 	ext{VFX (09)} \longrightarrow 	ext{Shader (10)} \longrightarrow 	ext{UI (11)} \longrightarrow 	ext{Prefab (12)} \longrightarrow 	ext{QA (13)} \longrightarrow 	ext{Ash Archive Commit (14)}$$

1. **01 — Concept**: Establish thematic intent, spectral constant alignment, and narrative purpose.
2. **02 — Silhouette Lock**: Validate readability at 32×32, 64×64, or 128×128 pixel scales against high-contrast backgrounds.
3. **03 — Material Design**: Define Hard Noir physical material properties (Lithic, Obsidian, Titanium-Gold, Bio-Silicate).
4. **04 — Diffuse**: Author base 32-bit color index using canonical palette matrices.
5. **05 — Height**: Generate 8-bit greyscale displacement maps for relief lighting.
6. **06 — Normal**: Compute tangent-space normal maps from height data for 2D dynamic point lights.
7. **07 — Emission**: Author dual-channel RGB emission maps for spectral constant flaring.
8. **08 — Animation**: Rig and sequence keyframes at locked 12/24 FPS intervals.
9. **09 — VFX**: Bind particle emitters and mesh trails to designated attachment sockets.
10. **10 — Shader**: Assign custom GLSL/GDShader materials (Bayer dither, chromatic aberration, damage flash).
11. **11 — UI / Codex**: Render 256px/128px/64px detail plates and inventory tooltips.
12. **12 — Runtime Prefab**: Assemble `.tscn` packed scene in Godot 4 with collisions, hitboxes, and state controllers.
13. **13 — QA**: Execute 60 Hz performance budget verification, hitbox collision checks, and memory profiling.
14. **14 — Canonical Archive**: Commit asset metadata, hash signatures, and provenance records to the Ash Archive SQLite DAG Ledger under the Never-Overwrite Doctrine.
