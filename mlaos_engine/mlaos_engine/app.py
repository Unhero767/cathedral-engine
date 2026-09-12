import asyncio
import json
from typing import Dict, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.outbound_queue: asyncio.Queue = asyncio.Queue()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: Dict):
        """Enqueues message into non-blocking broadcast queue."""
        await self.outbound_queue.put(message)

    async def broadcast_worker(self):
        """Dedicated consumer task that drains outbound queue without holding reader threads."""
        while True:
            message = await self.outbound_queue.get()
            payload = json.dumps(message)
            disconnected = []
            
            # Fan out to all active connections
            for ws in list(self.active_connections):
                try:
                    await ws.send_text(payload)
                except Exception:
                    disconnected.append(ws)

            for ws in disconnected:
                self.disconnect(ws)
            self.outbound_queue.task_done()

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    # Run the outbound broadcaster worker in the background
    asyncio.create_task(manager.broadcast_worker())

@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Non-blocking async frame receipt
            data = await websocket.receive_json()
            
            # Process state mutation / trigger telemetry response
            event_type = data.get("action")
            if event_type == "telemetry_tick":
                await manager.broadcast({
                    "type": "mlaos:frequency-shift",
                    "phi": data.get("phi", 0.0),
                    "status": "processed"
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
