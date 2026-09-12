import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CODEX_DIR = BASE_DIR / "codex"

def load_all_strata() -> dict:
    """Loads Stratum I and II into a unified dictionary."""
    unified_codex = {"strata": [], "propositions": {}}
    
    for file in sorted(CODEX_DIR.glob("*.json")):
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                stratum_id = data.get("stratum", 1)
                stratum_name = data.get("name", f"Stratum {stratum_id}")
                unified_codex["strata"].append({
                    "id": stratum_id,
                    "name": stratum_name
                })
                
                # Ingest verses format
                if "verses" in data:
                    for verse in data["verses"]:
                        prop_id = verse.get("verse_id")
                        unified_codex["propositions"][prop_id] = {
                            "id": prop_id,
                            "text": verse.get("claim"),
                            "stratum": stratum_id,
                            "contradicts": []
                        }
                # Ingest books format
                for book in data.get("books", []):
                    for prop in book.get("propositions", []):
                        prop["stratum"] = stratum_id
                        prop["book"] = book["book"]
                        unified_codex["propositions"][prop["id"]] = prop
            except Exception:
                continue
                    
    return unified_codex

def get_contradictions(prop_id: str) -> list:
    codex = load_all_strata()
    prop = codex["propositions"].get(prop_id, {})
    return prop.get("contradicts", [])

class CodexLoader:
    def __init__(self, codex_dir: Path = CODEX_DIR):
        self.codex_dir = codex_dir

    def load_all_strata(self) -> dict:
        return load_all_strata()

    def get_all_propositions(self) -> list:
        codex = load_all_strata()
        return list(codex["propositions"].values())
