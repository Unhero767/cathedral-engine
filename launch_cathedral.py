#!/usr/bin/env python3
import subprocess
import sys
import time
import socket

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def find_available_port(start_port: int) -> int:
    port = start_port
    while is_port_in_use(port):
        port += 1
    return port

def launch():
    print("[CATHEDRAL ENGINE] Booting Sovereign Substrates...")

    api_port = 8000 if not is_port_in_use(8000) else find_available_port(8001)
    web_port = 8080 if not is_port_in_use(8080) else find_available_port(8081)

    api_process = subprocess.Popen(["uvicorn", "mlaos_telemetry_service:app", "--host", "0.0.0.0", "--port", str(api_port)])
    time.sleep(1.0)
    server_process = subprocess.Popen([sys.executable, "-m", "http.server", str(web_port)])

    print("[CATHEDRAL ENGINE] Substrates online:")
    print(f" -> Telemetry Gateway: http://localhost:{api_port}")
    print(f" -> Spatial Lattice Visualizer: http://localhost:{web_port}/experiments/telemetry_visualizer.html")

    try:
        api_process.wait()
        server_process.wait()
    except KeyboardInterrupt:
        print("\n[CATHEDRAL ENGINE] Shutting down substrates gracefully.")
        api_process.terminate()
        server_process.terminate()

if __name__ == "__main__":
    launch()
