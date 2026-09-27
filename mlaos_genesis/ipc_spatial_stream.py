import asyncio
import json
import logging
import socket

logging.basicConfig(level=logging.INFO, format="[IPC BRIDGE] %(asctime)s - %(levelname)s - %(message)s")

class SpatialIPCBroadcaster:
    def __init__(self, host="127.0.0.1", port=8001):
        self.host = host
        self.port = port
        self.clients = set()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        logging.info(f"Godot simulation runtime connected from {addr}")
        self.clients.add(writer)
        
        try:
            handshake = json.dumps({
                "source": "Cathedral-Engine-Core",
                "status": "IPC_STREAM_ACTIVE",
                "message": "Spatial binding established. Ready for Belnap-Dunn telemetry."
            }) + "\n"
            writer.write(handshake.encode('utf-8'))
            await writer.drain()

            while True:
                data = await reader.read(1024)
                if not data:
                    break
                message = data.decode('utf-8').strip()
                logging.info(f"Received engine telemetry acknowledgment: {message}")
                
        except asyncio.CancelledError:
            pass
        finally:
            logging.info(f"Godot simulation runtime disconnected: {addr}")
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast_telemetry(self, entity_id: str, ontological_state: str, incurred_cost: float):
        if not self.clients:
            logging.warning("No active Godot simulation clients connected to IPC stream.")
            return

        payload = json.dumps({
            "entity_id": entity_id,
            "belnap_state": ontological_state,
            "incurred_cost": incurred_cost
        }) + "\n"

        encoded = payload.encode('utf-8')
        for writer in list(self.clients):
            try:
                writer.write(encoded)
                await writer.drain()
                logging.info(f"Transmitted spatial payload for {entity_id} [State: {ontological_state}]")
            except Exception as e:
                logging.error(f"Failed to transmit to client: {e}")
                self.clients.remove(writer)

    async def start_server(self):
        # Explicitly configure socket reuse to prevent address collision errors
        loop = asyncio.get_running_loop()
        server = await loop.create_server(
            lambda: asyncio.StreamReaderProtocol(asyncio.StreamReader(), self.handle_client),
            self.host,
            self.port,
            reuse_address=True,
            reuse_port=True
        )
        
        addr = server.sockets[0].getsockname()
        logging.info(f"Spatial IPC streaming server active on {addr}")
        
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    broadcaster = SpatialIPCBroadcaster()
    try:
        asyncio.run(broadcaster.start_server())
    except KeyboardInterrupt:
        logging.info("IPC streaming server terminated by operator.")
