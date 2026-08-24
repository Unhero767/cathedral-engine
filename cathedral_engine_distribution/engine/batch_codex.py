"""
Cathedral-Engine Full 40-Book Batch Chapter Scaffolder & Vault Compiler.
Generates and cryptographically anchors all 40 canonical monographs into ash_archive.db.
"""

from __future__ import annotations
import os
import json
import time
from typing import Dict, List, Any

from .database import DatabaseManager
from .codex_generator import CodexGenerator, CODEX_40_BOOKS_DATA
from .merkle_verifier import MerkleVerifier

class BatchCodexCompiler:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.generator = CodexGenerator(db)
        self.verifier = MerkleVerifier(db)

    def compile_all_40_books(self) -> Dict[str, Any]:
        """
        Scaffolds Chapter 1 for every book from Book I to Book XL,
        anchoring each into codex_chapters and the JBP ash_ledger DAG.
        """
        t0 = time.time()
        scaffolded_chapters: List[Dict[str, Any]] = []
        tier_counts = {"Prime Foundations": 0, "Inner Mandala": 0, "Outer Choirs": 0, "Inner Shadow Canon": 0}

        for book in CODEX_40_BOOKS_DATA:
            b_id = book["book_id"]
            tier = book["tier_designation"]
            
            # Scaffold canonical monograph
            chapter = self.generator.scaffold_chapter(book_id=b_id, chapter_num=1)
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
            
            scaffolded_chapters.append({
                "book_id": b_id,
                "roman_numeral": book["roman_numeral"],
                "title": book["title"],
                "tier": tier,
                "chapter_id": chapter.chapter_id,
                "content_hash": chapter.content_hash,
                "merkle_proof": chapter.merkle_proof,
                "parent_ledger_hash": chapter.parent_ledger_hash
            })

        elapsed = round(time.time() - t0, 3)

        # Run verification check
        verify_res = self.verifier.verify_ledger_chain()

        summary = {
            "total_books_scaffolded": len(scaffolded_chapters),
            "tier_distribution": tier_counts,
            "elapsed_seconds": elapsed,
            "merkle_verification": verify_res,
            "chapters": scaffolded_chapters
        }

        # Auto-refresh Vault Exports
        self._export_vault_artifacts()
        return summary

    def _export_vault_artifacts(self):
        out_dir = "/working_dir/c_9a0a4a350cc893af/artifacts"
        os.makedirs(out_dir, exist_ok=True)
        
        # 1. Master Codex
        codex_path = os.path.join(out_dir, "CODEX_40_BOOKS_MASTER_EXPORT.md")
        with open(codex_path, "w", encoding="utf-8") as f:
            f.write("# THE 40-BOOK CODEX OF MLAOS-PRIME (CANONICAL MONOGRAPHS)\n\n")
            f.write("Axiom: Emotion = Physics = Magic = Biology = Architecture\n\n")
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT s.book_id, s.roman_numeral, s.title, s.tier_designation, s.tier_range,
                       s.spectral_dominant, s.primary_axiom, s.isomorphism_bio, s.isomorphism_arch,
                       s.isomorphism_math, c.chapter_designation, c.content_hash, c.merkle_proof, c.full_monograph
                FROM codex_strata s
                LEFT JOIN codex_chapters c ON s.book_id = c.book_id
                ORDER BY s.book_id ASC
                """)
                for row in cursor.fetchall():
                    f.write(f"## {row['roman_numeral']}: {row['title']}\n")
                    f.write(f"- **Tier**: {row['tier_designation']} ({row['tier_range']})\n")
                    f.write(f"- **Spectral Dominant**: {row['spectral_dominant']}\n")
                    f.write(f"- **Primary Axiom**: {row['primary_axiom']}\n")
                    f.write(f"- **Biological Proof**: {row['isomorphism_bio']}\n")
                    f.write(f"- **Architectural Proof**: {row['isomorphism_arch']}\n")
                    f.write(f"- **Mathematical Proof**: {row['isomorphism_math']}\n")
                    if row["content_hash"]:
                        f.write(f"- **Content Hash**: `{row['content_hash']}`\n")
                        f.write(f"- **Merkle Proof**: `{row['merkle_proof']}`\n")
                    f.write("\n")
                    if row["full_monograph"]:
                        f.write("<details><summary>View Full Chapter Monograph</summary>\n\n")
                        f.write(row["full_monograph"] + "\n\n")
                        f.write("</details>\n\n")

        # 2. NotebookLM Vector Pack
        nlm_path = os.path.join(out_dir, "NOTEBOOKLM_HIGH_DENSITY_VECTOR_PACK.md")
        with open(nlm_path, "w", encoding="utf-8") as f:
            f.write("# MLAOS-PRIME CATHEDRAL-ENGINE NOTEBOOKLM VECTOR PACK (40 BOOKS)\n\n")
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM codex_strata ORDER BY book_id ASC")
                for row in cursor.fetchall():
                    f.write(f"> **DOMAIN**: Core Architecture / {row['tier_designation']}\n")
                    f.write(f"> **STRATUM**: {row['roman_numeral']} - {row['title']}\n")
                    f.write(f"> **SPECTRAL**: {row['spectral_dominant']}\n")
                    f.write(f"> **AXIOM**: {row['primary_axiom']}\n")
                    f.write(f"> **ISOMORPHISMS**: Bio: {row['isomorphism_bio']} | Arch: {row['isomorphism_arch']} | Math: {row['isomorphism_math']}\n\n")
