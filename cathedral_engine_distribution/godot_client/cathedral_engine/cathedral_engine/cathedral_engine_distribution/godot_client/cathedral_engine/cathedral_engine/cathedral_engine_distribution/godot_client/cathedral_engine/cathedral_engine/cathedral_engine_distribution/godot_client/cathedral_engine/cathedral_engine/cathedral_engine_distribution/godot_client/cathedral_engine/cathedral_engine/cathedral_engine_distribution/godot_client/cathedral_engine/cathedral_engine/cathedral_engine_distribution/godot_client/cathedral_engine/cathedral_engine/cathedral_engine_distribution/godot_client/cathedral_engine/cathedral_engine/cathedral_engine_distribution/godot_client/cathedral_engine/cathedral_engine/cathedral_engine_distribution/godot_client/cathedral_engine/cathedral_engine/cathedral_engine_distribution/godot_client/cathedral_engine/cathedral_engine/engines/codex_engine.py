import os
import json
import re
from typing import Dict, Any, List, Optional

CODEX_STRATA_MAP = {
    "Prime Foundations": list(range(1, 11)),
    "Inner Mandala": list(range(11, 21)),
    "Outer Choirs": list(range(21, 31)),
    "Shadow Canon": list(range(31, 41))
}

SPECTRAL_CONSTANTS = {
    "Gold": "Joy / Structure / Authority",
    "Teal": "Curiosity / Flow / Adaptability",
    "Blue": "Sorrow / Memory / Cognition",
    "Red": "Anger / Rupture / Motion",
    "Violet": "Fear / Transcendence / Becoming",
    "Emerald": "Love / Growth / Autopoiesis",
    "Obsidian": "Null / Void-Touch / Ash Archive"
}

class CodexManager:
    """
    40-Book Codex Architecture & Monograph Manager
    Maps structural strata, validates canonical formatting, generates NotebookLM corpora,
    and produces 4-part architectural monographs.
    """
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir
        self.codex_dir = os.path.join(base_dir, "codex")
        self.expanded_dir = os.path.join(os.path.dirname(base_dir), "expanded_chambers")
        os.makedirs(self.codex_dir, exist_ok=True)

    def get_stratum_for_book(self, book_num: int) -> str:
        """Determines the structural stratum for a given book index (1-40)."""
        for stratum, books in CODEX_STRATA_MAP.items():
            if book_num in books:
                return stratum
        return "Unmapped Canon"

    def list_books(self) -> List[Dict[str, Any]]:
        """Lists and catalogs all available books across codex/ and expanded_chambers/."""
        books = []
        files = []
        if os.path.exists(self.codex_dir):
            files.extend([os.path.join(self.codex_dir, f) for f in os.listdir(self.codex_dir) if f.endswith(('.md', '.txt'))])
        if os.path.exists(self.expanded_dir):
            files.extend([os.path.join(self.expanded_dir, f) for f in os.listdir(self.expanded_dir) if f.endswith(('.md', '.txt'))])

        seen = set()
        for filepath in sorted(files):
            fname = os.path.basename(filepath)
            if fname in seen:
                continue
            seen.add(fname)
            
            match = re.search(r'book_([0-9ivxlcdm]+)', fname, re.IGNORECASE)
            book_label = match.group(1).upper() if match else "?"
            
            size_b = os.path.getsize(filepath)
            books.append({
                "filename": fname,
                "path": filepath,
                "label": book_label,
                "size_bytes": size_b
            })
        return books

    def format_canonical_monograph(self, book_id: str, title: str, spectrum: str, payload_text: str) -> str:
        """
        Formats a raw book text or chapter into the canonical 4-Part Cathedral Codex Monograph:
        Section I: Opening Movement & Spectral Dominant
        Section II: Foundational Strata & Structural Anchors
        Section III: Dialetheic Buffer & Paraconsistent Collision
        Section IV: Synthesis & Harmonic Scar Integration
        """
        lines = [
            f"# Book {book_id}: {title}",
            "",
            "## Section I: Opening Movement & Spectral Dominant",
            f"- **Spectral Constant**: `{spectrum}` ({SPECTRAL_CONSTANTS.get(spectrum.split('/')[0], 'Active Calibration')})",
            "- **Liturgy of the State**: The architecture remembers the weight of all prior stresses without overwrite.",
            "",
            "## Section II: Foundational Strata & Structural Anchors",
            "- **Biological Anchor**: Autopoietic cellular regulation and somatic heat sink transduction.",
            "- **Architectural Anchor**: Flying buttresses, tensegrity arches, and interlocking permineralized masonry.",
            "- **Mathematical Anchor**: $\\nabla Ex \\oplus \\neg Ex = \\text{Harmonic Scar}_{\\tau}$.",
            "",
            "## Section III: Dialetheic Buffer & Paraconsistent Collision",
            payload_text.strip(),
            "",
            "## Section IV: Synthesis & Harmonic Scar Integration",
            "- **Permineralized Memory**: All fracture boundaries are integrated as permanent structural conduits.",
            "- **System Verdict**: State confirmed under the Decalogue of Immutable Law."
        ]
        return chr(10).join(lines)

    def build_notebooklm_corpus(self, output_path: Optional[str] = None) -> str:
        """Compiles all books, monographs, and strata into a single markdown corpus for NotebookLM ingestion."""
        if output_path is None:
            output_path = os.path.join(self.base_dir, "MLAOS_NOTEBOOKLM_MASTER_CORPUS.md")

        books = self.list_books()
        corpus_parts = [
            "# MLAOS-Prime & Cathedral-Engine Master Knowledge Corpus",
            "## Architectural Invariants, 40-Book Codex, and Dialetheic Canon",
            f"*Total Cataloged Manuscripts: {len(books)}*",
            "---"
        ]

        for b in books:
            try:
                with open(b["path"], "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                corpus_parts.append(chr(10) + f"# MANUSCRIPT: {b['filename']}" + chr(10))
                corpus_parts.append(content)
                corpus_parts.append(chr(10) + "---" + chr(10))
            except Exception as e:
                corpus_parts.append(chr(10) + f"[ERROR Reading {b['filename']}: {e}]" + chr(10))

        full_corpus = chr(10).join(corpus_parts)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_corpus)

        print(f"[CODEX] NotebookLM Master Corpus compiled at: {output_path} ({len(full_corpus)} chars)")
        return output_path

if __name__ == "__main__":
    mgr = CodexManager()
    all_books = mgr.list_books()
    print(f"[CODEX MANAGER] Found {len(all_books)} cataloged book manuscripts.")
    mgr.build_notebooklm_corpus()
