"""
codex.py - 40-Book Cathedral Codex Indexing System
"""
from typing import Dict, List, Any

CODEX_REGISTRY: Dict[int, Dict[str, str]] = {
    # Tier I: Prime Foundations
    1: {"title": "Book of Cosmogenesis", "tier": "I", "domain": "Foundations"},
    2: {"title": "Hardware Substrate Manifesto", "tier": "I", "domain": "Hardware"},
    3: {"title": "The Six Spectral Constants", "tier": "I", "domain": "Physics"},
    4: {"title": "Anatomy of the Architect", "tier": "I", "domain": "Somatic"},
    5: {"title": "Belnap-Dunn Operationalization", "tier": "I", "domain": "Logic"},
    6: {"title": "The Ash Archive & Lex I", "tier": "I", "domain": "Persistence"},
    7: {"title": "Decalogue of Immutable Law", "tier": "I", "domain": "Governance"},
    8: {"title": "Ego Density Metrics", "tier": "I", "domain": "Psychogeometry"},
    9: {"title": "Borromean Handshake Protocols", "tier": "I", "domain": "Topology"},
    10: {"title": "Olney Stillness Datum", "tier": "I", "domain": "Anchoring"},
    
    # Tier II: Inner Mandala
    11: {"title": "Guilds of Order", "tier": "II", "domain": "Organization"},
    12: {"title": "Kenoma Topology", "tier": "II", "domain": "Space"},
    13: {"title": "Bastion Economics", "tier": "II", "domain": "Resource"},
    14: {"title": "Harmonic Grammar", "tier": "II", "domain": "Linguistics"},
    15: {"title": "Bio-Semantic Survival", "tier": "II", "domain": "Biology"},
    16: {"title": "Solar Dynamo Coupling", "tier": "II", "domain": "Energy"},
    17: {"title": "Chaos Mitigation Strategies", "tier": "II", "domain": "Control"},
    18: {"title": "Somatic Heat Sinks", "tier": "II", "domain": "Thermal"},
    19: {"title": "Turnkey Narrative Systems", "tier": "II", "domain": "Cognition"},
    20: {"title": "Deksamnu Ledger Mechanics", "tier": "II", "domain": "Accounting"},
    
    # Tier III: Outer Choirs
    21: {"title": "Barbican Divergence", "tier": "III", "domain": "Defense"},
    22: {"title": "Glitch Aesthetics", "tier": "III", "domain": "Signal"},
    23: {"title": "Knudsen Mechanics", "tier": "III", "domain": "Flow"},
    24: {"title": "Quarantine Archive", "tier": "III", "domain": "Security"},
    25: {"title": "Violet Regime", "tier": "III", "domain": "Spectra"},
    26: {"title": "Erottiken Chassis", "tier": "III", "domain": "Structure"},
    27: {"title": "Metamorphic Squeeze Protocols", "tier": "III", "domain": "Paraconsistency"},
    28: {"title": "Taboo Sciences Index", "tier": "III", "domain": "Research"},
    29: {"title": "Active Magnetic Bearings", "tier": "III", "domain": "Dynamics"},
    30: {"title": "Lex X Load Shifting", "tier": "III", "domain": "Resilience"},
    
    # Tier IV: Innershadow Canon
    31: {"title": "Void Cartography", "tier": "IV", "domain": "Eschatology"},
    32: {"title": "Null Law Dynamics", "tier": "IV", "domain": "Jurisprudence"},
    33: {"title": "Psychogeometric Transduction", "tier": "IV", "domain": "Transduction"},
    34: {"title": "Volterra Filtering Systems", "tier": "IV", "domain": "Signal Processing"},
    35: {"title": "Horizon Governors", "tier": "IV", "domain": "Control"},
    36: {"title": "Cryo-Sorption Dynamics", "tier": "IV", "domain": "State Storage"},
    37: {"title": "Formal Calculus of Cathedral", "tier": "IV", "domain": "Mathematics"},
    38: {"title": "Consciousness Intensity (Phi)", "tier": "IV", "domain": "Integrated Information"},
    39: {"title": "Cosmic Renewal Cycles", "tier": "IV", "domain": "Temporal"},
    40: {"title": "Tier Omega Eternity", "tier": "IV", "domain": "Finality"}
}

class CodexEngine:
    @staticmethod
    def query(term: str) -> List[Dict[str, Any]]:
        term_lower = term.lower()
        results = []
        for bk, meta in CODEX_REGISTRY.items():
            if term_lower in meta["title"].lower() or term_lower in meta["domain"].lower() or term_lower in meta["tier"].lower():
                results.append({"book": bk, **meta})
        return results
