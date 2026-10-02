import json
import os
from typing import Dict, Any, List, Optional

class UniverseAtlasEngine:
    """
    Cathedral-Engine Cosmic Atlas & Universe Mapping Engine
    Manages structural telemetry across the 4 Strata, 40 Codex Monographs,
    36-Chambered Heart Oculus, 3 Sovereign Tri-Keys, and 7-Chroma Spectrum.
    """
    def __init__(self, manifest_path: Optional[str] = None):
        if manifest_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            manifest_path = os.path.join(base_dir, "config", "mlaos_universe_manifest.json")
        self.manifest_path = manifest_path
        self.universe_data = self._load_manifest()

    def _load_manifest(self) -> Dict[str, Any]:
        if os.path.exists(self.manifest_path):
            try:
                with open(self.manifest_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "universe_title": "MLAOS-Prime",
            "author": "Kenneth Dallmier",
            "anchor_telemetry": {
                "prime_geodetic_anchor": "Olney, IL",
                "carrier_frequency_hz": 43.7
            },
            "decalogue_of_immutable_laws": [],
            "chromatic_spectra": {},
            "sovereign_trikeys": [],
            "heart_oculus_36_chambers": {"ring_1_sensory": [], "ring_2_emotional": [], "ring_3_memory": []}
        }

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns fundamental universe constants and anchor coordinates."""
        return self.universe_data.get("anchor_telemetry", {})

    def get_laws(self) -> List[Dict[str, Any]]:
        """Returns the Decalogue of Immutable Laws (Lex I to Lex X)."""
        return self.universe_data.get("decalogue_of_immutable_laws", [])

    def get_chromatic_spectra(self) -> Dict[str, Any]:
        """Returns the 7-Chroma matrix with hex ranges and affinity relationships."""
        return self.universe_data.get("chromatic_spectra", {})

    def get_trikeys(self) -> List[Dict[str, Any]]:
        """Returns the three Sovereign Tri-Keys and their executive aspects."""
        return self.universe_data.get("sovereign_trikeys", [])

    def get_heart_oculus_rings(self) -> Dict[str, Any]:
        """Returns the 36 chambers of the Bio-Silicate Heart Oculus partitioned across 3 rings."""
        return self.universe_data.get("heart_oculus_36_chambers", {})

    def get_strata_overview(self) -> List[Dict[str, Any]]:
        """Returns high-level structural map across the 4 strata."""
        return self.universe_data.get("strata_overview", [])

    def get_full_atlas_summary(self) -> Dict[str, Any]:
        """Returns complete serializable universe manifest for Web Atlas and CLI renderers."""
        return {
            "title": self.universe_data.get("universe_title", "MLAOS-Prime"),
            "author": self.universe_data.get("author", "Kenneth Dallmier"),
            "anchor": self.get_telemetry(),
            "laws_count": len(self.get_laws()),
            "spectra_count": len(self.get_chromatic_spectra()),
            "trikeys_count": len(self.get_trikeys()),
            "oculus_total_chambers": 36,
            "strata": self.get_strata_overview()
        }

if __name__ == "__main__":
    atlas = UniverseAtlasEngine()
    print("[UNIVERSE ATLAS] Initialized. Summary:")
    summary = atlas.get_full_atlas_summary()
    print(json.dumps(summary, indent=2))
