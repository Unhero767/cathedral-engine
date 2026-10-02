#!/usr/bin/env python3
"""
Test .mlvox Validator Suite (test_mlvox_validate.py)
===================================================
Gate 03 Verification Harness
Validates clean passes (exit 0) and targeted corruptions across Layers 1, 2, 3, and 4.
"""

import hashlib
import json
import math
from pathlib import Path
import struct
import tempfile
import unittest

from mlvox_validate import (
    MLVoxValidator,
    MAGIC_BYTES,
    HEADER_STRUCT_FORMAT,
    HEADER_SIZE,
    VOXEL_STRUCT_FORMAT,
    VOXEL_STRIDE,
)

def build_mlvox_file(
    voxels=None,
    metadata=None,
    magic=MAGIC_BYTES,
    version=1,
    corrupt_hash=False,
    truncate=False,
) -> bytes:
    if voxels is None:
        voxels = [
            (0.0, 0.0, 0.0, 255, 215, 0, 1.0),
            (0.5, 0.5, 0.5, 120, 120, 120, 0.75),
        ]
    meta_bytes = json.dumps(metadata or {"author": "Kenneth Dallmier", "spec": "CE-003"}).encode("utf-8")
    voxel_bytes = b"".join(struct.pack(VOXEL_STRUCT_FORMAT, *v) for v in voxels)
    c_hash = hashlib.sha256(voxel_bytes).digest()

    if corrupt_hash:
        c_hash = b"\x00" * 32

    header = struct.pack(
        HEADER_STRUCT_FORMAT,
        magic,
        version,
        1,
        HEADER_SIZE,
        len(voxels),
        c_hash,
        len(meta_bytes),
    )
    raw = header + meta_bytes + voxel_bytes
    if truncate:
        raw = raw[: len(raw) - 10]
    return raw

class TestMLVoxValidatorLayers(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def test_layer_0_valid_file(self):
        file_path = self.temp_dir / "valid.mlvox"
        file_path.write_bytes(build_mlvox_file())
        report = MLVoxValidator(file_path).validate_all()
        self.assertTrue(report["valid"])
        self.assertEqual(report["exit_code"], 0)
        self.assertEqual(report["voxel_count"], 2)
        self.assertTrue(report["layer_1_structural"]["passed"])
        self.assertTrue(report["layer_2_scalar"]["passed"])
        self.assertTrue(report["layer_3_topological"]["passed"])
        self.assertTrue(report["layer_4_canonical"]["passed"])

    def test_layer_1_structural_corruptions(self):
        # Invalid magic bytes
        f_magic = self.temp_dir / "bad_magic.mlvox"
        f_magic.write_bytes(build_mlvox_file(magic=b"BAD_VOX!"))
        r_magic = MLVoxValidator(f_magic).validate_all()
        self.assertFalse(r_magic["valid"])
        self.assertEqual(r_magic["exit_code"], 1)

        # Unsupported version
        f_ver = self.temp_dir / "bad_version.mlvox"
        f_ver.write_bytes(build_mlvox_file(version=99))
        r_ver = MLVoxValidator(f_ver).validate_all()
        self.assertFalse(r_ver["valid"])
        self.assertEqual(r_ver["exit_code"], 1)

        # Truncated payload
        f_trunc = self.temp_dir / "truncated.mlvox"
        f_trunc.write_bytes(build_mlvox_file(truncate=True))
        r_trunc = MLVoxValidator(f_trunc).validate_all()
        self.assertFalse(r_trunc["valid"])
        self.assertEqual(r_trunc["exit_code"], 1)

    def test_layer_2_scalar_bounds(self):
        # Coordinate out of bounds (> 1.0)
        f_coord = self.temp_dir / "bad_coord.mlvox"
        f_coord.write_bytes(build_mlvox_file(voxels=[(2.5, 0.0, 0.0, 255, 255, 255, 1.0)]))
        r_coord = MLVoxValidator(f_coord).validate_all()
        self.assertFalse(r_coord["valid"])
        self.assertEqual(r_coord["exit_code"], 2)

        # Lumen intensity out of bounds (> 1.0)
        f_lumen = self.temp_dir / "bad_lumen.mlvox"
        f_lumen.write_bytes(build_mlvox_file(voxels=[(0.0, 0.0, 0.0, 255, 255, 255, 1.8)]))
        r_lumen = MLVoxValidator(f_lumen).validate_all()
        self.assertFalse(r_lumen["valid"])
        self.assertEqual(r_lumen["exit_code"], 2)

        # Non-finite scalar (NaN)
        f_nan = self.temp_dir / "nan_scalar.mlvox"
        f_nan.write_bytes(build_mlvox_file(voxels=[(float("nan"), 0.0, 0.0, 255, 255, 255, 0.5)]))
        r_nan = MLVoxValidator(f_nan).validate_all()
        self.assertFalse(r_nan["valid"])
        self.assertEqual(r_nan["exit_code"], 2)

    def test_layer_3_topological_duplicates(self):
        # Two voxels sharing the identical rounded coordinates (0.0, 0.0, 0.0)
        duplicate_voxels = [
            (0.00001, 0.0, 0.0, 255, 255, 255, 1.0),
            (0.00002, 0.0, 0.0, 100, 100, 100, 0.5),
        ]
        f_dup = self.temp_dir / "duplicate.mlvox"
        f_dup.write_bytes(build_mlvox_file(voxels=duplicate_voxels))
        r_dup = MLVoxValidator(f_dup).validate_all()
        self.assertFalse(r_dup["valid"])
        self.assertEqual(r_dup["exit_code"], 3)

    def test_layer_4_canonical_hash_mismatch(self):
        # Payload altered after computing canonical hash (modifying color channel)
        voxels = [
            (0.0, 0.0, 0.0, 255, 255, 255, 1.0),
            (0.3, 0.3, 0.3, 128, 128, 128, 0.5),
        ]
        meta_bytes = json.dumps({"spec": "CE-003"}).encode("utf-8")
        v_bytes = bytearray(b"".join(struct.pack(VOXEL_STRUCT_FORMAT, *v) for v in voxels))
        c_hash = hashlib.sha256(v_bytes).digest()

        # Modify one byte in voxel payload without updating header hash
        v_bytes[12] = 200

        header = struct.pack(
            HEADER_STRUCT_FORMAT,
            MAGIC_BYTES,
            1,
            1,
            HEADER_SIZE,
            len(voxels),
            c_hash,
            len(meta_bytes),
        )
        raw_tampered = header + meta_bytes + bytes(v_bytes)

        f_tampered = self.temp_dir / "tampered.mlvox"
        f_tampered.write_bytes(raw_tampered)
        r_tampered = MLVoxValidator(f_tampered).validate_all()
        self.assertFalse(r_tampered["valid"])
        self.assertEqual(r_tampered["exit_code"], 4)

if __name__ == "__main__":
    unittest.main()
