#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Paraconsistent Circuit Test Harness
# File: test_paraconsistent_circuit.py
# ==============================================================================

import json
import os
import hashlib
from datetime import datetime
from belnap_logic import BelnapValue, belnap_conjunction, belnap_disjunction, belnap_negation

def run_circuit_tests():
    print("[PARACON_TEST] Initializing Belnap-Dunn paraconsistent circuit test harness...")
    
    # Define complex circuit test vectors combining TRUE, FALSE, BOTH (dialetheic glut), and NEITHER (gap)
    test_circuits = [
        {"id": "CIRCUIT-01", "name": "Dialetheic Conjunction Glut", "input_a": BelnapValue.BOTH, "input_b": BelnapValue.FALSE, "gate": "AND"},
        {"id": "CIRCUIT-02", "name": "Truth-Value Gap Integration", "input_a": BelnapValue.NEITHER, "input_b": BelnapValue.TRUE, "gate": "OR"},
        {"id": "CIRCUIT-03", "name": "Recursive Negation Loop", "input_a": BelnapValue.BOTH, "input_b": BelnapValue.NEITHER, "gate": "NOT_A_AND_B"},
        {"id": "CIRCUIT-04", "name": "Absolute Dialetheic Synthesis", "input_a": BelnapValue.BOTH, "input_b": BelnapValue.BOTH, "gate": "OR"}
    ]
    
    circuit_records = []
    prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
    
    if os.path.exists("strata/paraconsistent_circuit_ledger.json"):
        with open("strata/paraconsistent_circuit_ledger.json", "r") as f:
            existing = json.load(f)
            if existing:
                prev_hash = existing[-1].get("block_hash", prev_hash)

    print(f"[PARACON_TEST] Evaluating {len(test_circuits)} paraconsistent circuit vectors...")

    for circuit in test_circuits:
        a = circuit["input_a"]
        b = circuit["input_b"]
        gate_type = circuit["gate"]
        
        # Compute paraconsistent logic outcome
        if gate_type == "AND":
            output_val = belnap_conjunction(a, b)
        elif gate_type == "OR":
            output_val = belnap_disjunction(a, b)
        elif gate_type == "NOT_A_AND_B":
            neg_a = belnap_negation(a)
            output_val = belnap_conjunction(neg_a, b)
        else:
            output_val = a

        payload = {
            "circuit_id": circuit["id"],
            "circuit_name": circuit["name"],
            "input_a": a.value,
            "input_b": b.value,
            "gate_operation": gate_type,
            "output_state": output_val.value,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        serialized = json.dumps(payload, sort_keys=True) + prev_hash
        block_hash = hashlib.sha256(serialized.encode('utf-8')).hexdigest()
        
        circuit_records.append({
            "prev_hash": prev_hash,
            "block_hash": block_hash,
            "metrics": payload
        })
        prev_hash = block_hash
        
        print(f"[CIRCUIT] [{circuit['id']}] {circuit['name']} ({a.value} {gate_type} {b.value}) -> Output: {output_val.value}")

    output_path = "strata/paraconsistent_circuit_ledger.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(circuit_records, f, indent=4)
        
    print(f"[PARACON_TEST] Circuit evaluation complete. Immutable ledger written to {output_path}.")

if __name__ == "__main__":
    run_circuit_tests()
