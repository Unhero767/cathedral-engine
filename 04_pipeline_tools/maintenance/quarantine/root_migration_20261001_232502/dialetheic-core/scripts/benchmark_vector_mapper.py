"""
Asset 7: VectorMapper Performance & Tension Benchmark Script.
Measures vector calculation throughput across proposition pairs.
"""

import time
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PARENT_DIR not in sys.path: sys.path.insert(0, PARENT_DIR)

from src.vector_mapper import VectorMapper

def run_benchmark():
    mapper = VectorMapper(vector_dim=64, seed=42)
    start_time = time.time()
    iterations = 500

    p_claim = "Every chamber is wholly filled with resonant stone and blazing light."
    p_counter = "Every chamber is wholly empty - no stone, no light, no witness."

    for _ in range(iterations):
        mapper.calculate_paradox_load(p_claim, p_counter)

    elapsed = time.time() - start_time
    ops_per_sec = iterations / elapsed
    print(f"=== VectorMapper Benchmark Result ===")
    print(f"Iterations : {iterations}")
    print(f"Elapsed    : {elapsed:.4f} seconds")
    print(f"Throughput : {ops_per_sec:.2f} evaluations/sec")

if __name__ == "__main__":
    run_benchmark()
