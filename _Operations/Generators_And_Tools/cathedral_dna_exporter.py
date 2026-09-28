#!/usr/bin/env python3
import sys, os, json, struct, hashlib, argparse
from typing import Dict, List, Tuple

CANONICAL_KEYS_128 = sorted([
    "adipose_distribution_abdominal_lower", "adipose_distribution_abdominal_upper",
    "adipose_distribution_brachial", "adipose_distribution_buccal",
    "adipose_distribution_cervical_posterior", "adipose_distribution_femoral_anterior",
    "adipose_distribution_femoral_posterior", "adipose_distribution_gluteal",
    "adipose_distribution_lumbar", "adipose_distribution_pectoral",
    "adipose_distribution_scapular", "adipose_distribution_subcutaneous_general",
    "adipose_distribution_sural", "adipose_distribution_temporal",
    "adipose_distribution_visceral", "adipose_distribution_zygomatic",
    "clearance_cranial_calvaria_offset", "clearance_cranial_cowl_margin",
    "clearance_femoral_chausse_gap", "clearance_femoral_poleyn_pitch",
    "clearance_girdle_reliquary_harness", "clearance_humeral_spaulder_standoff",
    "clearance_lumbar_fauld_expansion", "clearance_pectoral_cuirass_offset",
    "clearance_pelvic_tasset_articulation", "clearance_scapular_backplate_standoff",
    "clearance_sternal_plastron_flare", "clearance_sural_greave_clearance",
    "clearance_thoracic_gambeson_loft", "clearance_throat_gorget_circumference",
    "clearance_trapezius_mantle_rise", "clearance_waist_belt_cinch_tension",
    "cranial_glabella_prominence", "cranial_mandibular_angle",
    "cranial_mandibular_breadth", "cranial_mastoid_projection",
    "cranial_mental_protuberance", "cranial_nasal_aperture_width",
    "cranial_nasal_dorsum_height", "cranial_nasal_root_depression",
    "cranial_occipital_protuberance", "cranial_orbital_aperture_height",
    "cranial_orbital_breadth", "cranial_palatine_depth",
    "cranial_pyriform_flare", "cranial_vault_depth",
    "cranial_vault_height", "cranial_vault_width",
    "dermal_collagen_density", "dermal_elasticity_modulus",
    "dermal_epidermal_thickness", "dermal_erythema_basal",
    "dermal_melanin_concentration", "dermal_subsurface_lipid_ratio",
    "dermal_sweat_gland_porosity", "dermal_turgor_hydration",
    "hypertrophy_biceps_brachii", "hypertrophy_brachialis",
    "hypertrophy_brachioradialis", "hypertrophy_deltoid_anterior",
    "hypertrophy_deltoid_lateral", "hypertrophy_deltoid_posterior",
    "hypertrophy_erector_spinae", "hypertrophy_extensor_carpi_radialis",
    "hypertrophy_extensor_digitorum", "hypertrophy_flexor_carpi_ulnaris",
    "hypertrophy_gastrocnemius_lateral", "hypertrophy_gastrocnemius_medial",
    "hypertrophy_gluteus_maximus", "hypertrophy_gluteus_medius",
    "hypertrophy_infraspinatus", "hypertrophy_latissimus_dorsi",
    "hypertrophy_obliquus_externus", "hypertrophy_pectoralis_clavicular",
    "hypertrophy_pectoralis_major", "hypertrophy_pronator_teres",
    "hypertrophy_rectus_abdominis", "hypertrophy_rectus_femoris",
    "hypertrophy_rhomboid_major", "hypertrophy_serratus_anterior",
    "hypertrophy_soleus", "hypertrophy_sternocleidomastoid",
    "hypertrophy_teres_major", "hypertrophy_tibialis_anterior",
    "hypertrophy_trapezius_cervical", "hypertrophy_trapezius_thoracic",
    "hypertrophy_triceps_brachii", "hypertrophy_vastus_lateralis",
    "osteology_acromial_breadth", "osteology_bicristal_pelvic_width",
    "osteology_bitrochanteric_breadth", "osteology_brachial_index",
    "osteology_cervical_curvature_index", "osteology_clavicular_length",
    "osteology_crural_index", "osteology_femoral_bicondylar_width",
    "osteology_humeral_robusticity", "osteology_lumbar_lordosis_angle",
    "osteology_radial_torsion_angle", "osteology_ribcage_transverse_diameter",
    "osteology_sternal_length", "osteology_tibial_retroversion",
    "osteology_vertebral_column_length", "osteology_xiphoid_projection",
    "resonance_afield_conductance", "resonance_ash_accumulation_affinity",
    "resonance_bioelectric_potential", "resonance_cardiac_stroke_volume",
    "resonance_cognitive_strain_threshold", "resonance_corrosion_resistance",
    "resonance_dialetheic_buffer_capacity", "resonance_lumen_decay_half_life",
    "resonance_lumen_emission_peak", "resonance_metabolic_thermo_flux",
    "resonance_ocular_cyan_luminosity", "resonance_penitent_vocalization_gain",
    "resonance_somatic_armor_friction", "resonance_spectral_purity_theta",
    "resonance_synaptic_latency_index", "resonance_tissue_recuperation_rate",
    "vascularity_brachial_medial", "vascularity_cephalic_arm_left",
    "vascularity_cephalic_arm_right", "vascularity_dorsal_venous_left",
    "vascularity_dorsal_venous_right", "vascularity_femoral_great_saphenous",
    "vascularity_forearm_anterior", "vascularity_jugular_external"
])

PARAM_COUNT = 128
BUFFER_SIZE = 512

DEFAULT_ONTOLOGY_BOUNDS = {
    "cranial_vault_depth": (0.80, 1.30),
    "cranial_vault_width": (0.80, 1.30),
    "cranial_vault_height": (0.80, 1.30),
    "osteology_brachial_index": (0.70, 1.30),
    "osteology_crural_index": (0.70, 1.30),
    "osteology_lumbar_lordosis_angle": (0.0, 1.0),
    "resonance_dialetheic_buffer_capacity": (0.0, 2.0),
    "resonance_afield_conductance": (0.0, 2.0),
}

def export_recipe_to_dna(recipe_path: str, output_dna_path: str) -> Tuple[str, str]:
    with open(recipe_path, "r", encoding="utf-8") as f:
        recipe = json.load(f)
    raw_params = recipe.get("anatomical_parameters", {})
    float_array = [0.0] * PARAM_COUNT

    for i, key in enumerate(CANONICAL_KEYS_128):
        val = float(raw_params.get(key, 0.0))
        min_b, max_b = DEFAULT_ONTOLOGY_BOUNDS.get(key, (0.0, 1.0))
        float_array[i] = max(min_b, min(max_b, val))

    dna_bytes = struct.pack(f"<{PARAM_COUNT}f", *float_array)
    sha256 = hashlib.sha256(dna_bytes).hexdigest()

    with open(output_dna_path, "wb") as f:
        f.write(dna_bytes)
    return output_dna_path, sha256

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("recipe_json")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    out_path = args.output or os.path.splitext(args.recipe_json)[0] + ".dna"
    export_recipe_to_dna(args.recipe_json, out_path)
    print(f"[EXPORT SUCCESS] Wrote 512 bytes to {out_path}")
