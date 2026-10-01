from __future__ import annotations

from typing import Any, Dict


class ArbiterMagister:
    """Read-only narrative and liturgical arbiter observing Ash Archive DAG commits."""

    SPECTRAL_PRIORITIES = {
        "POST_RUPTURE_VITRIFIED": "NULL",
        "CRITICAL": "PHI",
        "DIALETHEIC_COLLISION": "DELTA",
        "SCAR_CRYSTALLIZED": "EPSILON",
        "VERIFIED": "THETA",
        "RECURSIVE": "PSI",
    }

    def ingest_committed_node(self, node: Any) -> Dict[str, str]:
        delta = getattr(node, "state_delta", {})
        scars = getattr(node, "harmonic_scars", [])
        cascade = getattr(node, "cascade_event", None)
        height = getattr(node, "block_height", 0)
        leaf_hash = getattr(node, "merkle_leaf_hash", "0" * 64)

        if cascade is not None:
            spectral_dominant = self.SPECTRAL_PRIORITIES["POST_RUPTURE_VITRIFIED"]
            tone = "RUPTURE_VITRIFICATION"
        elif len(scars) > 0:
            spectral_dominant = self.SPECTRAL_PRIORITIES["SCAR_CRYSTALLIZED"]
            tone = "KINTSUGI_MORTAR"
        elif delta.get("strain", 0.0) >= 4.0:
            spectral_dominant = self.SPECTRAL_PRIORITIES["CRITICAL"]
            tone = "METAMORPHIC_TENSION"
        else:
            spectral_dominant = self.SPECTRAL_PRIORITIES["VERIFIED"]
            tone = "AXIOMATIC_CALM"

        action = delta.get("action", "REST_STATE")
        strain = delta.get("strain", 0.0)
        liturgy = (
            f"Litany of Block {height} [{spectral_dominant} Dominant]: "
            f"The action '{action}' was compiled under {tone}. "
            f"Substrate strain stabilized at {strain:.2f}/5.00. "
            f"Harmonic scars committed: {len(scars)}. "
            f"Domain rupture occurred: {cascade is not None}."
        )

        chamber_log = (
            f"[ASH_LOG::H{height:04d}] NodeID: {node.node_id} | "
            f"Leaf: {leaf_hash[:12]}... | MerkleRoot: {node.parent_hash[:12]}... | "
            f"Domain: {node.domain} | Stratum: {node.stratum}"
        )

        return {
            "spectral_dominant": spectral_dominant,
            "liturgical_tone": tone,
            "liturgical_synthesis": liturgy,
            "chamber_log": chamber_log,
        }
