"""
Interactive Terminal REPL Shell - Cathedral-Engine Dialetheic Core Command Interface.
Allows real-time command execution, scar inspection, dialectic ingestion, and node sync.
"""

import os
import sys
import requests

API_BASE = "http://127.0.0.1:8000"

def run_repl():
    print("=" * 72)
    print(" CATHEDRAL-ENGINE :: INTERACTIVE TERMINAL SHELL (REPL)")
    print("=" * 72)
    print(" Commands: ingest, sync, query, state, scars, book2, batch, exit\n")

    while True:
        try:
            cmd_input = input("\033[96m[CATHEDRAL-SHELL] > \033[0m").strip()
            if not cmd_input:
                continue

            parts = cmd_input.split(maxsplit=1)
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if cmd in ["exit", "quit", "q"]:
                print("Exiting Cathedral Shell.")
                break

            elif cmd == "state":
                res = requests.get(f"{API_BASE}/state")
                print(res.json())

            elif cmd == "scars":
                res = requests.get(f"{API_BASE}/scars")
                print(res.json())

            elif cmd == "book2":
                res = requests.post(f"{API_BASE}/codex/ingest/book2")
                print(res.json())

            elif cmd == "query":
                key = args or "mlaos.outer_choir.mythos.syntax_of_the_unborn"
                res = requests.get(f"{API_BASE}/query?key={key}")
                print(res.json())

            elif cmd == "ingest":
                print("Enter Claim (P):")
                claim = input("  Claim > ").strip()
                print("Enter Counter-Claim (NOT P):")
                counter = input("  Counter-Claim > ").strip()
                if claim and counter:
                    res = requests.post(f"{API_BASE}/ingest", json={
                        "verse_id": "SHELL-INGEST",
                        "claim": claim,
                        "counter_claim": counter
                    })
                    print("\nIngestion Result:")
                    print(res.json())

            elif cmd == "sync":
                load = float(args) if args else 8.42
                res = requests.post(f"{API_BASE}/node/sync", json={
                    "instance_id": "aurelia-12",
                    "mqi_score": 92.0,
                    "a_field_temperature_k": 308.0,
                    "current_flux": 2.5,
                    "active_spectrum": "BRONZE_OBSIDIAN",
                    "active_paradox_load": load
                })
                print(res.json())

            else:
                print(f"Unknown command: '{cmd}'. Valid: state, scars, ingest, sync, query, book2, exit")

        except KeyboardInterrupt:
            print("\nExiting Cathedral Shell.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_repl()
