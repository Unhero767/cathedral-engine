#!/usr/bin/env python3
import os, json
from cathedral_dna_exporter import export_recipe_to_dna

ARCHETYPES = [
    {
        "specimen_id": "CT-OMEGA-01",
        "archetype_name": "Crucible Templar",
        "caste": "Melee Vanguard",
        "spectral_constant": "JOY_GOLD_THETA",
        "dialetheic_afield": 0.87,
        "master_texture_path": "res://assets/portraits/master_atlas_strip.png",
        "silhouette_preset": "templar_plate",
        "anatomical_parameters": {
            "adipose_distribution_visceral": 0.85,
            "cranial_vault_depth": 1.15,
            "hypertrophy_pectoralis_major": 0.90,
            "resonance_afield_conductance": 1.45,
            "resonance_ocular_cyan_luminosity": 0.92
        }
    },
    {
        "specimen_id": "NA-NULL-02",
        "archetype_name": "Null Astrologer",
        "caste": "Entropic Weaver",
        "spectral_constant": "VOID_OBSIDIAN_NULL",
        "dialetheic_afield": 1.25,
        "master_texture_path": "res://assets/portraits/master_atlas_strip.png",
        "silhouette_preset": "astrologer_robes",
        "anatomical_parameters": {
            "adipose_distribution_visceral": 0.15,
            "cranial_vault_depth": 1.35,
            "dermal_melanin_concentration": 0.85,
            "resonance_dialetheic_buffer_capacity": 1.85
        }
    },
    {
        "specimen_id": "PM-DELTA-03",
        "archetype_name": "Penitent Monad",
        "caste": "Ascetic Anchor",
        "spectral_constant": "SORROW_BLUE_DELTA",
        "dialetheic_afield": 0.60,
        "master_texture_path": "res://assets/portraits/master_atlas_strip.png",
        "silhouette_preset": "ascetic_hood",
        "anatomical_parameters": {
            "adipose_distribution_visceral": 0.70,
            "dermal_collagen_density": 0.80,
            "osteology_lumbar_lordosis_angle": 0.60
        }
    },
    {
        "specimen_id": "SS-PSI-04",
        "archetype_name": "Sovereign Seraph",
        "caste": "Cognitive Vanguard",
        "spectral_constant": "CURIOSITY_TEAL_PSI",
        "dialetheic_afield": 1.50,
        "master_texture_path": "res://assets/portraits/master_atlas_strip.png",
        "silhouette_preset": "seraph_halo",
        "anatomical_parameters": {
            "cranial_vault_depth": 1.10,
            "resonance_ocular_cyan_luminosity": 2.20,
            "resonance_synaptic_latency_index": 0.95
        }
    },
    {
        "specimen_id": "CB-PHI-05",
        "archetype_name": "Crucible Berserk",
        "caste": "Shock Vanguard",
        "spectral_constant": "ANGER_CRIMSON_PHI",
        "dialetheic_afield": 1.10,
        "master_texture_path": "res://assets/portraits/master_atlas_strip.png",
        "silhouette_preset": "berserk_bulk",
        "anatomical_parameters": {
            "hypertrophy_deltoid_lateral": 1.20,
            "hypertrophy_pectoralis_major": 1.15,
            "vascularity_forearm_anterior": 0.95
        }
    },
    {
        "specimen_id": "VA-EPSILON-06",
        "archetype_name": "Verdant Anchor",
        "caste": "Biological Grounding",
        "spectral_constant": "LOVE_EMERALD_EPSILON",
        "dialetheic_afield": 0.95,
        "master_texture_path": "res://assets/portraits/master_atlas_strip.png",
        "silhouette_preset": "verdant_organic",
        "anatomical_parameters": {
            "cranial_vault_depth": 1.00,
            "dermal_turgor_hydration": 0.95,
            "resonance_tissue_recuperation_rate": 1.80
        }
    },
    {
        "specimen_id": "AS-OMEGA-07",
        "archetype_name": "Ash Scourge",
        "caste": "Monastic Penitent",
        "spectral_constant": "FEAR_VIOLET_OMEGA",
        "dialetheic_afield": 1.30,
        "master_texture_path": "res://assets/portraits/master_atlas_strip.png",
        "silhouette_preset": "scourge_gaunt",
        "anatomical_parameters": {
            "resonance_ash_accumulation_affinity": 1.95,
            "clearance_cranial_calvaria_offset": 0.30
        }
    },
    {
        "specimen_id": "VS-VOID-08",
        "archetype_name": "Void Sovereign",
        "caste": "Cosmic Arbiter",
        "spectral_constant": "NULL_OBSIDIAN_VOID",
        "dialetheic_afield": 1.95,
        "master_texture_path": "res://assets/portraits/master_atlas_strip.png",
        "silhouette_preset": "void_sovereign",
        "anatomical_parameters": {
            "cranial_vault_depth": 1.40,
            "resonance_afield_conductance": 2.00,
            "resonance_ocular_cyan_luminosity": 2.50,
            "resonance_spectral_purity_theta": 2.00
        }
    }
]

os.makedirs("archetypes", exist_ok=True)
for arch in ARCHETYPES:
    slug = arch["archetype_name"].lower().replace(" ", "_")
    j_path = f"archetypes/{slug}.json"
    d_path = f"archetypes/{slug}.dna"
    with open(j_path, "w") as f:
        json.dump(arch, f, indent=2)
    export_recipe_to_dna(j_path, d_path)
    print(f"[BAKED ARCHETYPE] {arch['archetype_name']:18s} -> {d_path}")
