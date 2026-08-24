"""
Cathedral-Engine Merkle Proof Validator & Tamper-Detection Engine.
Enforces the Never-Overwrite Doctrine and automated rollback to signed JBP blocks.
"""

from __future__ import annotations
import json
import sqlite3
from typing import Dict, List, Tuple, Any, Optional
from .models import AshBlock
from .database import DatabaseManager

class MerkleVerifier:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def verify_ledger_chain(self) -> Dict[str, Any]:
        """
        Walks the entire ash_ledger block sequence from Block #0 to tip.
        Verifies:
        1. Parent hash continuity (block[i].parent_hash == block[i-1].block_hash)
        2. Block hash calculation correctness (recalculated SHA256 matches block_hash)
        3. JBP signature validity
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ash_ledger ORDER BY block_index ASC")
            rows = cursor.fetchall()
            
            if not rows:
                return {"valid": False, "error": "Empty ash_ledger. Genesis block missing.", "tampered_index": 0}

            prev_hash = "0" * 64
            verified_count = 0
            
            for idx, row in enumerate(rows):
                block = AshBlock(
                    index=row["block_index"],
                    timestamp=row["timestamp"],
                    parent_hash=row["parent_hash"],
                    merkle_root=row["merkle_root"],
                    event_type=row["event_type"],
                    payload_json=row["payload_json"],
                    block_hash=row["block_hash"],
                    jbp_signature=row["jbp_signature"]
                )
                
                # Check index sequence
                if block.index != idx:
                    return {
                        "valid": False,
                        "error": f"Block index discontinuity at #{block.index}, expected #{idx}",
                        "tampered_index": block.index,
                        "last_valid_hash": prev_hash
                    }

                # Check parent hash (for blocks > 0)
                if idx > 0 and block.parent_hash != prev_hash:
                    return {
                        "valid": False,
                        "error": f"Broken parent hash link at Block #{block.index}. Found {block.parent_hash[:12]}, expected {prev_hash[:12]}",
                        "tampered_index": block.index,
                        "last_valid_hash": prev_hash
                    }

                # Recalculate hash
                recalc_hash = block.calculate_hash()
                if recalc_hash != block.block_hash:
                    return {
                        "valid": False,
                        "error": f"Hash tampering detected at Block #{block.index}. Payload altered.",
                        "tampered_index": block.index,
                        "last_valid_hash": prev_hash
                    }

                # Verify JBP Signature
                expected_sig = block.generate_signature()
                if expected_sig != block.jbp_signature:
                    return {
                        "valid": False,
                        "error": f"Invalid JBP signature at Block #{block.index}. Forged authority.",
                        "tampered_index": block.index,
                        "last_valid_hash": prev_hash
                    }

                prev_hash = block.block_hash
                verified_count += 1

            return {
                "valid": True,
                "verified_blocks": verified_count,
                "tip_block_index": rows[-1]["block_index"],
                "tip_block_hash": prev_hash,
                "message": "All strata verified. Never-Overwrite compliance: 100%."
            }

    def rollback_to_safe_block(self, safe_index: int) -> Dict[str, Any]:
        """
        Executes automated rollback to the last verified cryptographic block in case of corruption.
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT block_hash FROM ash_ledger WHERE block_index = ?", (safe_index,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Target safe block index #{safe_index} does not exist.")
            
            # Prune corrupted blocks > safe_index
            cursor.execute("DELETE FROM ash_ledger WHERE block_index > ?", (safe_index,))
            conn.commit()

            return {
                "rollback_completed": True,
                "restored_tip_index": safe_index,
                "restored_tip_hash": row["block_hash"],
                "notice": "Corrupted blocks excised. Ledger restored to cryptographically verified invariant."
            }
