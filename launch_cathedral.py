import subprocess
import sys
import time

def launch():
    print("[CATHEDRAL ENGINE] Booting Sovereign Substrates...")
    api_process = subprocess.Popen(["uvicorn", "mlaos_telemetry_service:app", "--host", "0.0.0.0", "--port", "8000"])
    time.sleep(1.0)
    server_process = subprocess.Popen([sys.executable, "-m", "http.server", "8080"])
    print("[CATHEDRAL ENGINE] Substrates online:")
    print(" -> Telemetry Gateway: http://localhost:8000")
    print(" -> Spatial Lattice Visualizer: http://localhost:8080/experiments/telemetry_visualizer.html")
    try:
        api_process.wait()
        server_process.wait()
    except KeyboardInterrupt:
        print("\n[CATHEDRAL ENGINE] Shutting down substrates gracefully.")
        api_process.terminate()
        server_process.terminate()

if __name__ == "__main__":
    launch()
