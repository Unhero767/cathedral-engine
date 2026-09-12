# tests/test_spiral.py
from mlaos_prime.archive import AshArchiveMerkleDAG
from mlaos_prime.lattice import TruthValue
from mlaos_prime.spiral import RecursionGovernor, SpiralLexicon

def test_psi1_every_branch_has_lineage():
    lex = SpiralLexicon(AshArchiveMerkleDAG())
    a, _ = lex.ask("ROOT", "what branches from silence?")
    a1, _ = lex.ask(a.node_id, "does lineage hold at depth two?")
    assert [b.node_id for b in lex.lineage(a1.node_id)] == ["ROOT", a.node_id, a1.node_id]

def test_rg_psi_depth_cap_archives_refusal():
    arc = AshArchiveMerkleDAG()
    lex = SpiralLexicon(arc, RecursionGovernor(max_depth=2))
    a, _ = lex.ask("ROOT", "q1"); b, _ = lex.ask(a.node_id, "q2")
    refused, code = lex.ask(b.node_id, "q3")
    assert refused is None and code == "DEPTH_CAP"
    assert len(arc) == 1 and arc.verify()          # the refusal permineralizes; nothing lost

def test_cycle_detection():
    lex = SpiralLexicon(AshArchiveMerkleDAG())
    a, _ = lex.ask("ROOT", "does the spiral repeat?")
    assert lex.ask(a.node_id, "does the spiral repeat?")[1] == "CYCLE"

def test_contradiction_routes_to_buffer_as_scar():
    lex = SpiralLexicon(AshArchiveMerkleDAG())
    a, _ = lex.ask("ROOT", "can both hold?")
    s = lex.evaluate(a.node_id, 0.9, 0.8)
    assert s.logic_state is TruthValue.BOTH and s.outcome == "HARMONIC_SCAR"