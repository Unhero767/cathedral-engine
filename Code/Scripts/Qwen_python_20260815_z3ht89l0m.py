# mlaos_prime/spiral.py — the Spiral Lexicon & Recursion Governor RG-Ψ
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from .archive import AshArchiveMerkleDAG
from .lattice import TruthValue, collide
from .somatic import BASELINE_BPM, somatic_lock


@dataclass(frozen=True)
class Branch:
    """Ψ₁ made flesh: lineage is not a courtesy, it is a field."""
    node_id: str
    parent_id: Optional[str]
    question: str
    spectral: str
    logic_state: TruthValue
    confidence: float
    outcome: Optional[str] = None
    archive_ref: Optional[str] = None


class RecursionGovernor:
    """RG-Ψ — the leash is woven from the same basalt as the law."""

    def __init__(self, max_depth: int = 7, max_branches: int = 377,
                 paradox_threshold: float = 3.0) -> None:
        self.max_depth = max_depth
        self.max_branches = max_branches
        self.paradox_threshold = paradox_threshold
        self._seen: Set[Tuple[Optional[str], str]] = set()
        self.refusals: Dict[str, int] = {}

    def admit(self, parent_id, question, depth, paradox,
              ancestor_questions: List[str]) -> Tuple[bool, str]:
        if paradox > self.paradox_threshold:
            return self._refuse("SOMATIC_RETURN")
        if depth > self.max_depth:
            return self._refuse("DEPTH_CAP")
        if len(self._seen) >= self.max_branches:
            return self._refuse("BRANCH_CAP")
        if question in ancestor_questions:
            return self._refuse("CYCLE")
        if (parent_id, question) in self._seen:
            return self._refuse("DUPLICATE")
        self._seen.add((parent_id, question))
        return True, "ADMITTED"

    def _refuse(self, code: str) -> Tuple[bool, str]:
        self.refusals[code] = self.refusals.get(code, 0) + 1
        return False, code


class SpiralLexicon:
    """State → Question → Branch → Test → Consequence → Archive → New Question."""

    def __init__(self, archive: AshArchiveMerkleDAG,
                 governor: Optional[RecursionGovernor] = None) -> None:
        self.archive = archive
        self.governor = governor or RecursionGovernor()
        self._nodes: Dict[str, Branch] = {}
        self._children: Dict[str, List[str]] = {}
        self._depth: Dict[str, int] = {}
        root = Branch("ROOT", None, "axiom :: triad_sealed", "∅", TruthValue.TRUE, 1.0)
        self._nodes[root.node_id] = root
        self._depth[root.node_id] = 0

    def lineage(self, node_id: str) -> List[Branch]:
        chain, cur = [], node_id
        while cur is not None:
            b = self._nodes[cur]
            chain.append(b)
            cur = b.parent_id
        return list(reversed(chain))

    def ask(self, parent_id: str, question: str, spectral: str = "Ψ",
            confidence: float = 0.5, paradox: float = 0.0) -> Tuple[Optional[Branch], str]:
        depth = self._depth[parent_id] + 1
        ancestors = [b.question for b in self.lineage(parent_id)]
        ok, code = self.governor.admit(parent_id, question, depth, paradox, ancestors)
        if not ok:  # refused, not deleted — Lex I holds even for the unborn
            self.archive.append_scar(0.0, 0.0, f"rg_psi :: refused :: {code} :: {question}", spectral)
            return None, code
        node_id = f"{parent_id}·Ψ{len(self._children.get(parent_id, [])) + 1}"
        branch = Branch(node_id, parent_id, question, spectral, TruthValue.NONE, confidence)
        self._nodes[node_id] = branch
        self._children.setdefault(parent_id, []).append(node_id)
        self._depth[node_id] = depth
        return branch, "ADMITTED"

    def evaluate(self, node_id: str, c_pos: float, c_neg: float, n_vectors: int = 1) -> Branch:
        """Contradictions route through the Dialetheic Buffer; nothing crashes, everything settles."""
        b = self._nodes[node_id]
        if c_pos > 0.5 and c_neg > 0.5:
            state, outcome = collide(TruthValue.TRUE, TruthValue.FALSE), "HARMONIC_SCAR"
        elif c_pos >= c_neg:
            state, outcome = TruthValue.TRUE, "COHERENT"
        else:
            state, outcome = TruthValue.FALSE, "FRACTURE"
        ref = self.archive.append_scar(c_pos, c_neg, f"spiral :: {node_id} :: {b.question}",
                                       b.spectral, n_vectors).digest
        settled = Branch(b.node_id, b.parent_id, b.question, b.spectral,
                         state, b.confidence, outcome, ref)
        self._nodes[node_id] = settled
        return settled

    def settle(self, operator_bpm: float = BASELINE_BPM) -> bool:
        """Return control to 1.5 Hz before the spiral turns again."""
        return somatic_lock(operator_bpm)