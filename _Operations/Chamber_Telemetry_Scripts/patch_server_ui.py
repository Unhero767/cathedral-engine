with open("server.py", "r", encoding="utf-8") as f:
    code = f.read()

ROOT_HANDLER = '''        if path in ("/", "/index.html"):
            try:
                with open("index.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                self._send_json({"error": "Failed to read index.html", "details": str(e)}, 500)
                return
'''

if 'if path in ("/", "/index.html"):' not in code:
    code = code.replace("if path == \"/api/rpg/state\":", ROOT_HANDLER + "\n        elif path == \"/api/rpg/state\":")
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("[✓] server.py patched to serve index.html on http://localhost:5050/")

