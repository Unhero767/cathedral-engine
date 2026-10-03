"""
Cathedral-Engine: Gate 3 Test
Verifies ProofCarryingObject response validation and serialization invariants.
"""
import pytest
import time
from pydantic import ValidationError
from api.pco_envelopes import EpistemicRegisterTag, ProvenanceModel, ProofCarryingObjectResponse

def test_pco_envelope_valid_serialization():
    prov = ProvenanceModel(
        source="SensorArray:Omega-01",
        tau=time.time(),
        tick=4096,
        actor="ArbiterNode-Alpha",
        signature="ed25519_canonical_sig",
        context="Spire.Resonance",
        latency_delta=0.012
    )

    pco = ProofCarryingObjectResponse(
        value={"strain_tensor": [0.12, 0.44, 0.98]},
        provenance=prov,
        merkle_lineage="7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
        epistemic_register=EpistemicRegisterTag.SCAR,
        uncertainty_metadata={"kenomic_entropy": 52.4, "belnap_fog": 1}
    )

    dumped = pco.model_dump()
    assert dumped["epistemic_register"] == "S"
    assert dumped["provenance"]["context"] == "Spire.Resonance"
    assert dumped["uncertainty_metadata"]["belnap_fog"] == 1

def test_pco_envelope_rejects_invalid_register():
    prov = ProvenanceModel(
        source="SensorArray:Omega-01",
        tau=time.time(),
        tick=4096,
        actor="ArbiterNode-Alpha",
        signature="sig",
        context="Spire.Resonance",
        latency_delta=0.012
    )

    with pytest.raises(ValidationError):
        ProofCarryingObjectResponse(
            value={"data": True},
            provenance=prov,
            merkle_lineage="genesis",
            epistemic_register="INVALID_REGISTER",
            uncertainty_metadata={}
        )
