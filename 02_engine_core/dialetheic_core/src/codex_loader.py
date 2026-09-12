import json
import os
from pathlib import Path
from typing import List, Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent
CODEX_DIR = BASE_DIR / "codex"

class CodexLoader:
    def __init__(self, codex_dir: Path = CODEX_DIR):
        self.codex_dir = codex_dir

    def load_all_strata(self) -> List[Dict[str, Any]]:
        strata = []
        if not self.codex_dir.exists():
            return strata

        for file_path in sorted(self.codex_dir.glob("*.json")):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    strata.append(json.load(f))
                except json.JSONDecodeError:
                    continue
        return strata

    def get_all_propositions(self) -> List[Dict[str, Any]]:
        propositions = []
        for stratum in self.load_all_strata():
            if "verses" in stratum:
                for verse in stratum["verses"]:
                    propositions.append({
                        "id": verse.get("verse_id"),
                        "claim": verse.get("claim"),
                        "counter_claim": verse.get("counter_claim"),
                        "spectral_affinity": verse.get("spectral_affinity", "TEAL"),
                        "stratum": stratum.get("stratum", 1)
                    })
            elif "books" in stratum:
                for book in stratum["books"]:
                    for prop in book.get("propositions", []):
                        propositions.append({
                            "id": prop.get("id"),
                            "claim": prop.get("claim"),
                            "counter_claim": prop.get("counter_claim"),
                            "spectral_affinity": prop.get("spectral_affinity", "VIOLET"),
                            "contradicts": prop.get("contradicts", []),
                            "severity": prop.get("severity", 0.5),
                            "stratum": stratum.get("stratum", 2)
                        })
        return propositions
