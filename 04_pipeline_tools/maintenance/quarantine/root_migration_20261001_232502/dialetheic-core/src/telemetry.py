import asyncio
import json
from datetime import datetime
from typing import Set, Dict, Any
from fastapi import Request
from starlette.responses import StreamingResponse

class TelemetryHub:
    def __init__(self):
        self.listeners: Set[asyncio.Queue] = set()

    def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        self.listeners.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue):
        if queue in self.listeners:
            self.listeners.remove(queue)

    async def broadcast(self, event_type: str, data: Dict[str, Any]):
        payload = json.dumps({"type": event_type, "data": data}, default=str)
        for queue in list(self.listeners):
            try:
                await queue.put(payload)
            except Exception:
                self.unsubscribe(queue)

    async def event_generator(self, request: Request):
        queue = self.subscribe()
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield f"data: {data}\n\n"
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
        finally:
            self.unsubscribe(queue)

    def create_stream_response(self, request: Request) -> StreamingResponse:
        return StreamingResponse(
            self.event_generator(request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*"
            }
        )

telemetry_hub = TelemetryHub()
