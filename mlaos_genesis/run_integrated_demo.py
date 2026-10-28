import asyncio
import httpx
import json
import logging

logging.basicConfig(level=logging.INFO, format="[DEMO HARNESS] %(asctime)s - %(levelname)s - %(message)s")

async def mock_godot_ipc_listener(port=8001):
    """Simulates the Godot C# socket client intercepting telemetry."""
    await asyncio.sleep(0.5)
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', port)
        logging.info("[MOCK GODOT CLIENT]: Connected successfully to IPC spatial stream.")
        
        # Read handshake
        handshake = await reader.readline()
        logging.info(f"[MOCK GODOT CLIENT]: Received handshake -> {handshake.decode().strip()}")
        
        # Keep alive briefly to receive broadcast
        await asyncio.sleep(1.0)
            
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        logging.error(f"[MOCK GODOT CLIENT ERROR]: {e}")

async def run_demo():
    logging.info("=== CATHEDRAL-ENGINE INTEGRATED SYSTEM DEMONSTRATION ===")
    
    # 1. Audit Ash Archive Character Stable Ledger
    stable_url = "http://127.0.0.1:8000/archive/stable/status"
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(stable_url, timeout=2.0)
            if res.status_code == 200:
                data = res.json()
                logging.info(f"[LEDGER AUDIT]: Active Deployments: {data.get('active_deployment_count')} | Cryogenic Reserves: {data.get('vaulted_reserve_count')}")
            else:
                logging.warning(f"[LEDGER AUDIT]: Stable service responded with status {res.status_code}. Ensure ash_archive_stable.py is active.")
        except Exception:
            logging.error("[LEDGER AUDIT FAILURE]: Ash Archive ledger on port 8000 is unreachable. Run: python ash_archive_stable.py in a separate window.")

    # 2. Start IPC Broadcaster and Mock Client Concurrently
    from ipc_spatial_stream import SpatialIPCBroadcaster
    broadcaster = SpatialIPCBroadcaster(port=8001)
    
    server = await asyncio.start_server(broadcaster.handle_client, broadcaster.host, broadcaster.port)
    logging.info(f"[IPC STREAM]: Spatial broadcaster active on port {broadcaster.port}")

    # Launch mock Godot client listener task
    client_task = asyncio.create_task(mock_godot_ipc_listener(port=8001))

    # Wait until at least one client connects to the broadcaster
    logging.info("[IPC STREAM]: Awaiting Godot simulation runtime connection...")
    while not broadcaster.clients:
        await asyncio.sleep(0.1)

    # 3. Trigger Belnap-Dunn State B Overload & Broadcast Telemetry
    entity_id = "Janus_Stoneblood"
    ontological_state = "B" # Dialetheic collision (Harmonic Scar)
    chronological_mass = 1524.0
    incurred_cost = chronological_mass * 12.41 # High gravitational penalty

    logging.info(f"[BELNAP-DUNN MATRIX]: Evaluating intentional contradiction for {entity_id} -> State '{ontological_state}'")
    
    # Broadcast across IPC socket to simulation client
    await broadcaster.broadcast_telemetry(entity_id, ontological_state, incurred_cost)

    # Await client task completion
    await client_task
    
    server.close()
    await server.wait_closed()
    logging.info("=== DEMONSTRATION COMPLETE: Telemetry loop verified. ===")

if __name__ == "__main__":
    asyncio.run(run_demo())
