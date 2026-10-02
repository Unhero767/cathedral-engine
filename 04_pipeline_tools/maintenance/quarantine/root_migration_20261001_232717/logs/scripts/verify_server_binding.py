import sys
import os

# Ensure current directory is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from fastapi import FastAPI
    from scripts.patch_terminal_webhook import register_terminal_webhook
    
    app = FastAPI(title="Cathedral Engine Test Instance")
    register_terminal_webhook(app)
    
    # Verify the route was correctly added to FastAPI routing table
    routes = [route.path for route in app.routes]
    target_route = "/api/terminal/webhook"
    
    if target_route in routes:
        print(f"[Verification SUCCESS] Route '{target_route}' successfully bound to FastAPI routing table.")
        sys.exit(0)
    else:
        print(f"[Verification ERROR] Route '{target_route}' missing from registered routes: {routes}", file=sys.stderr)
        sys.exit(1)

except Exception as e:
    print(f"[Verification EXCEPTION] Failed during server binding check: {e}", file=sys.stderr)
    sys.exit(1)
