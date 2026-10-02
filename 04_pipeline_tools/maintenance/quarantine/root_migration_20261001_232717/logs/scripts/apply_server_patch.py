# Server Integration Patch for Terminal Webhook
# To be appended or imported into server.py

from scripts.patch_terminal_webhook import register_terminal_webhook

def apply_patch(app):
    """
    Binds the terminal webhook listener route to the active FastAPI app instance.
    """
    register_terminal_webhook(app)
    print("[Patch] Terminal webhook successfully bound to FastAPI routing table.")

if __name__ == "__main__":
    print("[Patch Module] Ready for import into server.py.")
