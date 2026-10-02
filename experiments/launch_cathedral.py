import http.server
import socketserver
import threading
import uvicorn
import os
import sys

# Ensure root directory is in sys.path and current working directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)

def run_uvicorn():
    uvicorn.run("mlaos_telemetry_service:app", host="0.0.0.0", port=8000, log_level="warning")

def run_http():
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"[Cathedral Launcher] HTTP server active at http://localhost:{PORT}/experiments/telemetry_visualizer.html")
        httpd.serve_forever()

if __name__ == "__main__":
    print("[Cathedral Launcher] Initializing Unified Substrates...")
    
    t1 = threading.Thread(target=run_uvicorn, daemon=True)
    t2 = threading.Thread(target=run_http, daemon=True)
    
    t1.start()
    print("[Cathedral Launcher] Ash Archive Telemetry Gateway online on port 8000.")
    t2.start()
    
    print("\n[Cathedral Launcher] All systems operational. Press Ctrl+C to halt.\n")
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\n[Cathedral Launcher] Sealing Cathedral sub-systems.")
