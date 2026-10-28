#!/usr/bin/env python3
"""
MLAOS-Prime: Automated Pytest Verification Suite for Book XXII Dossier
Run via: pytest tests/test_n_t_b_dossier.py -v --maxfail=1
"""

import sqlite3
import time
import pytest
from tests.verify_n_t_b_dossier import ParaconsistentStratumValidator


@pytest.fixture
def validator():
    return ParaconsistentStratumValidator(db_path=":memory:")


def test_n_to_t_to_b_canonical_trajectory(validator):
    target = "vault.axiom.042"
    state, vec, chain = validator.evaluate_stratum(target)
    assert state == "N" and vec == [0, 0] and len(chain) == 0

    res_t = validator.inscribe(target, "P", "tx_01H8X9A", "+1", 1793218620, "0x9a8f")
    assert res_t["transition"] == "N -> T"
    assert res_t["epistemic_state"] == "T"
    assert res_t["truth_vector"] == [1, 0]
    assert res_t["d_phi_dt"] == 1.420

    res_b = validator.inscribe(target, "P", "tx_01H8X9Z", "-1", 1793218624, "0x3c7b")
    assert res_b["transition"] == "T -> B"
    assert res_b["epistemic_state"] == "B"
    assert res_b["truth_vector"] == [1, 1]
    assert res_b["d_phi_dt"] == 4.891
    assert res_b["harmonic_scar"]["scar_id"] == "scar_8841_alpha"
    assert res_b["harmonic_scar"]["explosion_contained"] is True
    assert len(res_b["evidence_chain"]) == 2
    assert res_b["merkle_root"] == "0x1322be852940c384e8bc357bff45c9b99eedc6935c7353bf747a82076195a783"


def test_n_to_f_to_b_dual_trajectory(validator):
    target = "vault.axiom.099"
    res_f = validator.inscribe(target, "Q", "tx_neg_1", "-1", 1793219000, "0x1111")
    assert res_f["transition"] == "N -> F"
    assert res_f["epistemic_state"] == "F"
    assert res_f["truth_vector"] == [0, 1]
    assert res_f["spectral_signature"] == "BLUE_SORROW"

    res_b = validator.inscribe(target, "Q", "tx_pos_1", "+1", 1793219005, "0x2222")
    assert res_b["transition"] == "F -> B"
    assert res_b["epistemic_state"] == "B"
    assert res_b["truth_vector"] == [1, 1]


def test_lex_i_never_overwrite_triggers(validator):
    target = "vault.axiom.042"
    validator.inscribe(target, "P", "tx_immutable", "+1", 1793218620, "0x9a8f")

    with pytest.raises(sqlite3.IntegrityError, match="LEX_I_VIOLATION"):
        validator.conn.execute(
            "UPDATE ash_archive_evidence SET polarity = '-1' WHERE tx_id = 'tx_immutable'"
        )

    with pytest.raises(sqlite3.IntegrityError, match="LEX_I_VIOLATION"):
        validator.conn.execute(
            "DELETE FROM ash_archive_evidence WHERE tx_id = 'tx_immutable'"
        )


def test_paraconsistent_contagion_isolation(validator):
    validator.inscribe("vault.axiom.042", "P", "tx_1", "+1", 100, "0x1")
    validator.inscribe("vault.axiom.042", "P", "tx_2", "-1", 101, "0x2")

    adj_state, adj_vec, adj_chain = validator.evaluate_stratum("vault.axiom.043")
    assert adj_state == "N"
    assert adj_vec == [0, 0]
    assert len(adj_chain) == 0


def test_gate_3_p99_latency_under_12ms(validator):
    latencies_ms = []
    for i in range(100):
        stratum = f"vault.bench.{i // 2}"
        polarity = "+1" if i % 2 == 0 else "-1"
        t0 = time.perf_counter()
        validator.inscribe(stratum, "P", f"tx_bench_{i}", polarity, 1793218620 + i, "0xsig")
        latencies_ms.append((time.perf_counter() - t0) * 1000.0)

    latencies_ms.sort()
    p99_ms = latencies_ms[98]
    assert p99_ms < 12.0, f"Gate 3 Latency SLA breached: p99={p99_ms:.3f}ms >= 12.0ms"
