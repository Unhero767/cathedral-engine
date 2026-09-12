import asyncio
import json
import os
import threading
import time
from typing import Dict, Any, Optional
from websockets.asyncio.server import serve

class AshArchiveLedger:
    """Enforces immutable append-only persistence for Harmonic Scars and state strata."""
    def __init__(self, filepath: str = "ash_archive_strata.jsonl"):
        self.filepath = filepath
        self._lock = threading.Lock()
        if not os.path.exists(self.filepath):
            open(self.filepath, "w", encoding="utf-8").close()

    def append_scar(self, key: str, reason: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        record = {
            "timestamp": time.time(),
            "key": key,
            "reason": reason,
            "metadata": metadata or {}
        }
        with self._lock:
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")


class TelemetryEngine:
    """Calculates Consciousness Intensity Vector with EMA smoothing."""
    def __init__(self, alpha: float = 0.2):
        self.last_phi: float = 0.0
        self.last_time: float = time.time()
        self.smoothed_velocity: float = 0.0
        self.alpha: float = alpha

    def update(self, current_phi: float) -> Dict[str, Any]:
        now = time.time()
        dt = max(now - self.last_time, 0.0001)
        d_phi = current_phi - self.last_phi
        raw_velocity = d_phi / dt

        self.smoothed_velocity = (self.alpha * raw_velocity) + ((1.0 - self.alpha) * self.smoothed_velocity)
        self.last_phi = current_phi
        self.last_time = now

        frequency = self._resolve_frequency(current_phi)
        return {
            "phi": current_phi,
            "velocity": self.smoothed_velocity,
            "frequency_constant": frequency
        }

    def _resolve_frequency(self, phi: float) -> str:
        if phi > 7.5:
            return "Gold/Joy"
        elif phi > 4.0:
            return "Teal/Curiosity"
        else:
            return "Blue/Sorrow"


# Initialize singleton state
ledger = AshArchiveLedger()
telemetry = TelemetryEngine()
connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    print(f"[MLAOS-Prime] Client connected: {websocket.remote_address}")
    try:
        async for raw_message in websocket:
            data = json.loads(raw_message)
            action = data.get("action")
            
            if action == "telemetry_tick":
                phi = float(data.get("phi", 0.0))
                metrics = telemetry.update(phi)
                response = json.dumps({"type": "mlaos:frequency-shift", **metrics})
                
                # Echo metrics back to client and broadcast to all subscribers
                await websocket.send(response)
                for client in connected_clients:
                    if client != websocket:
                        await client.send(response)
            
            elif action == "crystallize_scar":
                ledger.append_scar(data.get("key"), data.get("reason"), data.get("metadata"))
                await websocket.send(json.dumps({"status": "scar_crystallized"}))
    except Exception as e:
        print(f"[MLAOS-Prime] Connection error: {e}")
    finally:
        connected_clients.remove(websocket)
        print(f"[MLAOS-Prime] Client disconnected: {websocket.remote_address}")

async def main():
    async with serve(handler, "127.0.0.1", 8765):
        print("[MLAOS-Prime] WebSocket Server active on ws://127.0.0.1:8765")
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[MLAOS-Prime] Terminating server session...")
