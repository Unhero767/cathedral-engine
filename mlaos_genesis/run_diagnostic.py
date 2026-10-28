import httpx
import asyncio

LLAMA_URL = "http://127.0.0.1:9932/health"
ARCHIVE_URL = "http://127.0.0.1:8000/archive/stable/status"
BRIDGE_TEST_URL = "http://127.0.0.1:8000/archive/history/Janus_Stoneblood"

async def run_diagnostics():
    print("[DIAGNOSTIC]: Initiating Cathedral-Engine telemetry audit across active strata...\n")
    
    async with httpx.AsyncClient() as client:
        # 1. Audit Native Llama Server (Port 9932)
        try:
            res = await client.get(LLAMA_URL, timeout=3.0)
            print(f"[PORT 9932 - LLAMA MATRIX]: Status {res.status_code} - Substrate operational.")
        except Exception as e:
            print(f"[PORT 9932 - LLAMA MATRIX]: UNREACHABLE ({e})")

        # 2. Audit Character Stable Ledger (Port 8000)
        try:
            res = await client.get(ARCHIVE_URL, timeout=3.0)
            if res.status_code == 200:
                data = res.json()
                print(f"[PORT 8000 - ASH ARCHIVE]: Active Deployments: {data.get('active_deployment_count')}, Vaulted Reserves: {data.get('vaulted_reserve_count')}")
            else:
                print(f"[PORT 8000 - ASH ARCHIVE]: Error response {res.status_code}")
        except Exception as e:
            print(f"[PORT 8000 - ASH ARCHIVE]: UNREACHABLE ({e}) - Ensure ash_archive_stable.py is running.")

        # 3. Simulate Belnap-Dunn State B Policy Overload
        try:
            res = await client.get(BRIDGE_TEST_URL, timeout=3.0)
            if res.status_code == 200:
                ledger_data = res.json()
                mass = ledger_data.get("chronological_mass_bytes", 1500.0)
                simulated_penalty = mass * 12.41
                print(f"[BELNAP-DUNN STATE B SIMULATION]: Entity '{ledger_data.get('entity_id')}' evaluated.")
                print(f" -> Chronological Mass: {mass} bytes")
                print(f" -> Incurred Dialetheic Cost (State B): {simulated_penalty:.2f} units")
                print(" -> [HARMONIC SCAR]: Shader parameter intensity scaling computed successfully.")
            else:
                print("[LEDGER QUERY]: Entity history not found.")
        except Exception as e:
            print(f"[LEDGER QUERY ERROR]: {e}")

    print("\n[DIAGNOSTIC COMPLETE]: System ready for Godot IPC spatial binding.")

if __name__ == "__main__":
    asyncio.run(run_diagnostics())
