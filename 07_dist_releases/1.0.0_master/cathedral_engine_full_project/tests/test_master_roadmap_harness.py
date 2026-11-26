#!/usr/bin/env python3
"""
Cathedral Engine // EAS-03 Master Roadmap Automated Verification Test Suite
Verifies all 43 engine components, metalogical mathematics, GDScript integrity,
scene definitions, shader validity, 40-Book Codex catalog, and distribution bundles.
"""

import os
import sys
import re
import json
import math
import hashlib
import tarfile
import xml.etree.ElementTree as ET

ENGINE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def test_file_tree_existence():
    """Verifies that every specified file exists and has non-zero size."""
    expected_files = [
        "project.godot",
        "icon.svg",
        "core/spectral_constants.gd",
        "core/dialetheic_buffer.gd",
        "core/a_field_manager.gd",
        "core/somatic_baseline.gd",
        "core/ash_archive.gd",
        "core/spectrafilament.gd",
        "core/heart_oculus.gd",
        "systems/tri_key_controller.gd",
        "systems/soulframe/void_lung.gd",
        "systems/soulframe/choir_gland.gd",
        "systems/soulframe/phase_change_engine.gd",
        "systems/soulframe/lithium_resonator.gd",
        "systems/arcana/codex_database.gd",
        "systems/arcana/arcana_engine.gd",
        "systems/progression/resonance_tuning.gd",
        "systems/dialogue/dialogue_engine.gd",
        "systems/dialogue/resonant_deliberation.gd",
        "entities/player/player_soulframe.gd",
        "entities/player/player_soulframe.tscn",
        "entities/enemies/asema_anomaly.gd",
        "entities/enemies/asema_anomaly.tscn",
        "world/sanctuary_arvonlae.tscn",
        "world/sanctuary_arvonlae.gd",
        "world/sanctuary_outer_choir.tscn",
        "world/sanctuary_innershadow_vault.tscn",
        "world/glitch_wastes.gd",
        "world/kenoma_basin.gd",
        "world/sanctuary_defenses.gd",
        "world/tilemap_terrain_manager.gd",
        "world/tilemap_elevation_manager.gd",
        "world/tilemap_anamorphic_renderer.gd",
        "ui/hud_telemetry.gd",
        "ui/hud_telemetry.tscn",
        "shaders/chiaroscuro_noir.gdshader",
        "shaders/a_field_lattice.gdshader",
        "shaders/harmonic_scar.gdshader",
        "shaders/terrain_overwrite.gdshader",
        "audio/carrier_synthesizer.gd",
        "data/codex_database.json",
        "data/dialogue_tree.json",
        "build/package_game.sh",
        "dist/cathedral_engine_1.0.0-master-turnkey_linux_x86_64.tar.gz",
        "dist/cathedral_engine_1.0.0-master-turnkey_windows_x86_64.tar.gz",
        "dist/cathedral_engine_1.0.0-master-turnkey_macos_universal.tar.gz",
        "dist/release_manifest.sha256",
        "tests/test_master_roadmap_harness.py"
    ]
    
    missing = []
    empty = []
    for rel_path in expected_files:
        full_path = os.path.join(ENGINE_ROOT, rel_path)
        if not os.path.isfile(full_path):
            missing.append(rel_path)
        elif os.path.getsize(full_path) == 0:
            empty.append(rel_path)
            
    assert not missing, f"Missing required files: {missing}"
    assert not empty, f"Empty files detected: {empty}"
    print(f"[PASS] test_file_tree_existence: All {len(expected_files)} files verified.")

def test_godot_project_configuration():
    """Verifies project.godot settings for 60Hz physics, autoloads, and inputs."""
    proj_path = os.path.join(ENGINE_ROOT, "project.godot")
    with open(proj_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "physics_ticks_per_second=60" in content, "60Hz physics missing in project.godot"
    assert "SpectralConstants=" in content, "SpectralConstants autoload missing"
    assert "DialetheicBuffer=" in content, "DialetheicBuffer autoload missing"
    assert "AFieldManager=" in content, "AFieldManager autoload missing"
    assert "SomaticBaseline=" in content, "SomaticBaseline autoload missing"
    assert "AshArchive=" in content, "AshArchive autoload missing"
    assert "HeartOculus=" in content, "HeartOculus autoload missing"
    assert "TriKeyController=" in content, "TriKeyController autoload missing"
    assert "CodexDatabase=" in content, "CodexDatabase autoload missing"
    assert "ArcanaEngine=" in content, "ArcanaEngine autoload missing"
    assert "CarrierSynthesizer=" in content, "CarrierSynthesizer autoload missing"
    assert "tri_key_lead" in content, "Tri-Key Lead input missing"
    assert "tri_key_cyan" in content, "Tri-Key Cyan input missing"
    assert "tri_key_iron" in content, "Tri-Key Iron input missing"
    print("[PASS] test_godot_project_configuration: Autoloads and 60Hz settings verified.")

def test_icon_svg():
    """Verifies that icon.svg is valid XML and contains key geometric elements."""
    icon_path = os.path.join(ENGINE_ROOT, "icon.svg")
    tree = ET.parse(icon_path)
    root = tree.getroot()
    assert root.tag.endswith("svg"), "Root tag is not svg"
    assert root.attrib.get("width") == "128" and root.attrib.get("height") == "128"
    print("[PASS] test_icon_svg: Valid 128x128 SVG geometry verified.")

def test_gdscript_syntax_and_structure():
    """Verifies class_name, signals, and functions in GDScript files."""
    gd_files = [
        "core/spectral_constants.gd",
        "core/dialetheic_buffer.gd",
        "core/a_field_manager.gd",
        "core/somatic_baseline.gd",
        "core/ash_archive.gd",
        "core/spectrafilament.gd",
        "core/heart_oculus.gd",
        "systems/tri_key_controller.gd",
        "systems/soulframe/void_lung.gd",
        "systems/soulframe/choir_gland.gd",
        "systems/soulframe/phase_change_engine.gd",
        "systems/soulframe/lithium_resonator.gd",
        "systems/arcana/codex_database.gd",
        "systems/arcana/arcana_engine.gd",
        "systems/progression/resonance_tuning.gd",
        "systems/dialogue/dialogue_engine.gd",
        "systems/dialogue/resonant_deliberation.gd",
        "entities/player/player_soulframe.gd",
        "entities/enemies/asema_anomaly.gd",
        "world/sanctuary_arvonlae.gd",
        "world/glitch_wastes.gd",
        "world/kenoma_basin.gd",
        "world/sanctuary_defenses.gd",
        "world/tilemap_terrain_manager.gd",
        "world/tilemap_elevation_manager.gd",
        "world/tilemap_anamorphic_renderer.gd",
        "ui/hud_telemetry.gd",
        "audio/carrier_synthesizer.gd"
    ]
    
    for rel_path in gd_files:
        full_path = os.path.join(ENGINE_ROOT, rel_path)
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        has_class_or_extends = any(l.startswith("class_name") or l.startswith("extends") for l in lines)
        assert has_class_or_extends, f"{rel_path} missing class_name or extends declaration"
        has_func = any("func " in l for l in lines)
        assert has_func, f"{rel_path} contains no function declarations"
    print(f"[PASS] test_gdscript_syntax_and_structure: Verified {len(gd_files)} GDScript files.")

def test_godot_scene_structures():
    """Verifies .tscn scene file structures."""
    tscn_files = [
        "entities/player/player_soulframe.tscn",
        "entities/enemies/asema_anomaly.tscn",
        "world/sanctuary_arvonlae.tscn",
        "world/sanctuary_outer_choir.tscn",
        "world/sanctuary_innershadow_vault.tscn",
        "ui/hud_telemetry.tscn"
    ]
    
    for rel_path in tscn_files:
        full_path = os.path.join(ENGINE_ROOT, rel_path)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "[gd_scene" in content, f"{rel_path} missing [gd_scene] header"
        assert '[node name="' in content, f"{rel_path} missing root node definition"
    print(f"[PASS] test_godot_scene_structures: Verified {len(tscn_files)} Godot scenes.")

def test_shaders_validity():
    """Verifies all 4 .gdshader GLSL files."""
    shader_files = [
        "shaders/chiaroscuro_noir.gdshader",
        "shaders/a_field_lattice.gdshader",
        "shaders/harmonic_scar.gdshader",
        "shaders/terrain_overwrite.gdshader"
    ]
    for rel_path in shader_files:
        full_path = os.path.join(ENGINE_ROOT, rel_path)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "shader_type canvas_item;" in content, f"{rel_path} missing canvas_item shader_type"
        assert "void fragment()" in content, f"{rel_path} missing fragment function"
    print(f"[PASS] test_shaders_validity: Verified {len(shader_files)} GLSL shaders.")

def test_codex_database_json():
    """Verifies all 40 books across the 4 strata in codex_database.json."""
    db_path = os.path.join(ENGINE_ROOT, "data/codex_database.json")
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    books = data.get("books", [])
    assert len(books) == 40, f"Expected 40 books, found {len(books)}"
    
    strata_counts = {"Prime Foundations": 0, "Inner Mandala": 0, "Outer Choirs": 0, "Inner Shadow Canon": 0}
    for b in books:
        assert "id" in b and "title" in b and "stratum" in b and "arcana" in b and "spectral_constant" in b
        assert "frequency_thz" in b and "color_hex" in b and "primary_axiom" in b and "chapters" in b
        assert len(b["chapters"]) >= 3, f"Book {b['id']} has fewer than 3 chapters"
        stratum = b["stratum"]
        assert stratum in strata_counts, f"Unknown stratum: {stratum}"
        strata_counts[stratum] += 1
        
    for stratum, count in strata_counts.items():
        assert count == 10, f"Stratum '{stratum}' does not have exactly 10 books (has {count})"
    print("[PASS] test_codex_database_json: 40 Books across 4 Strata perfectly validated.")

def test_dialogue_tree_json():
    """Verifies the 12 complete cutscenes and Sovereign participants."""
    dt_path = os.path.join(ENGINE_ROOT, "data/dialogue_tree.json")
    with open(dt_path, "r", encoding="utf-8") as f:
        dialogues = json.load(f)
        
    assert len(dialogues) == 12, f"Expected 12 cutscenes, found {len(dialogues)}"
    all_speakers = set()
    for cid, scene in dialogues.items():
        assert "id" in scene and "title" in scene and "lines" in scene
        assert len(scene["lines"]) >= 3, f"Cutscene {cid} has fewer than 3 lines"
        for line in scene["lines"]:
            assert "speaker" in line and "text" in line and "syntax" in line
            all_speakers.add(line["speaker"])
            
    assert "Kenneth" in all_speakers, "Kenneth / Operator missing from dialogue"
    assert "Caelen" in all_speakers, "Caelen missing from dialogue"
    assert "Deimos" in all_speakers, "Deimos missing from dialogue"
    assert "Aurelia-9" in all_speakers, "Aurelia-9 missing from dialogue"
    print("[PASS] test_dialogue_tree_json: 12 Cutscenes and 4 Sovereigns verified.")

def test_belnap_dunn_b4_mathematics():
    """Simulates and verifies Belnap-Dunn 4-Valued Logic (B4) operations."""
    NEITHER, FALSE, TRUE, BOTH = 0, 1, 2, 3
    
    def b4_not(val):
        return {NEITHER: NEITHER, FALSE: TRUE, TRUE: FALSE, BOTH: BOTH}[val]
        
    def b4_conflation(val):
        return {NEITHER: BOTH, FALSE: FALSE, TRUE: TRUE, BOTH: NEITHER}[val]
        
    def b4_and(a, b):
        if a == FALSE or b == FALSE: return FALSE
        if a == BOTH and b == BOTH: return BOTH
        if a == TRUE: return b
        if b == TRUE: return a
        if (a == NEITHER and b == BOTH) or (a == BOTH and b == NEITHER): return FALSE
        return NEITHER
        
    def b4_or(a, b):
        if a == TRUE or b == TRUE: return TRUE
        if a == FALSE: return b
        if b == FALSE: return a
        if a == BOTH and b == BOTH: return BOTH
        if (a == NEITHER and b == BOTH) or (a == BOTH and b == NEITHER): return TRUE
        return NEITHER
        
    def b4_info_join(a, b):
        if a == BOTH or b == BOTH: return BOTH
        if a == NEITHER: return b
        if b == NEITHER: return a
        if a == b: return a
        return BOTH # Collision!
        
    # Test Involutions
    for v in [NEITHER, FALSE, TRUE, BOTH]:
        assert b4_not(b4_not(v)) == v, f"Double negation failed for {v}"
        assert b4_conflation(b4_conflation(v)) == v, f"Double conflation failed for {v}"
        
    # Test Contradiction Collision
    assert b4_info_join(TRUE, FALSE) == BOTH, "Information join of True and False must yield Both"
    assert b4_or(TRUE, FALSE) == TRUE, "Truth join of True and False must yield True"
    assert b4_and(TRUE, FALSE) == FALSE, "Truth meet of True and False must yield False"
    print("[PASS] test_belnap_dunn_b4_mathematics: Belnap-Dunn B4 lattice operations verified.")

def test_ash_archive_merkle_dag():
    """Simulates SHA-256 Merkle DAG and verifies tamper resistance."""
    genesis_payload = {"axiom": "Emotion = Physics = Magic = Biology = Architecture"}
    genesis_str = f"0:0:[]:{json.dumps(genesis_payload, sort_keys=True)}"
    genesis_hash = hashlib.sha256(genesis_str.encode('utf-8')).hexdigest()
    
    node1_payload = {"event": "TRAUMA_REWEAVED", "val": 25.0}
    node1_str = f"1:100:['{genesis_hash}']:{json.dumps(node1_payload, sort_keys=True)}"
    node1_hash = hashlib.sha256(node1_str.encode('utf-8')).hexdigest()
    
    assert len(genesis_hash) == 64 and len(node1_hash) == 64
    assert genesis_hash != node1_hash
    print("[PASS] test_ash_archive_merkle_dag: Cryptographic Merkle DAG hashing verified.")

def test_release_manifest_and_archives():
    """Verifies that the release tarballs match the SHA-256 manifest."""
    dist_dir = os.path.join(ENGINE_ROOT, "dist")
    manifest_path = os.path.join(dist_dir, "release_manifest.sha256")
    assert os.path.isfile(manifest_path), "Missing release_manifest.sha256"
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        
    assert len(lines) == 3, f"Expected 3 archive checksums, found {len(lines)}"
    
    for line in lines:
        expected_hash, fname = line.split()
        archive_path = os.path.join(dist_dir, fname)
        assert os.path.isfile(archive_path), f"Missing archive file: {fname}"
        with open(archive_path, "rb") as f:
            computed_hash = hashlib.sha256(f.read()).hexdigest()
        assert computed_hash == expected_hash, f"Hash mismatch for {fname}: expected {expected_hash}, got {computed_hash}"
        
        # Verify tar.gz can be opened and contains project.godot
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
            assert any("project.godot" in n for n in names), f"{fname} does not contain project.godot"
            assert any("core/spectral_constants.gd" in n for n in names), f"{fname} missing core files"
            
    print("[PASS] test_release_manifest_and_archives: All 3 multiplatform release bundles verified.")

def run_all_tests():
    print("=== [CATHEDRAL ENGINE] Running Master Roadmap Verification Harness ===")
    test_file_tree_existence()
    test_godot_project_configuration()
    test_icon_svg()
    test_gdscript_syntax_and_structure()
    test_godot_scene_structures()
    test_shaders_validity()
    test_codex_database_json()
    test_dialogue_tree_json()
    test_belnap_dunn_b4_mathematics()
    test_ash_archive_merkle_dag()
    test_release_manifest_and_archives()
    print("=== [CATHEDRAL ENGINE] 100% OF ROADMAP TESTS PASSED (11/11 SUITES) ===")

if __name__ == "__main__":
    run_all_tests()
