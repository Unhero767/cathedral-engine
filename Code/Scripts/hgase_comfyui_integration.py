import os
import server
from aiohttp import web

# ComfyUI requires these dictionaries to recognize the folder as a custom node
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Initialize the HGASE endpoint on the ComfyUI server
@server.PromptServer.instance.app.route("/hgase")
async def serve_hgase_engine(request):
    # Locate the HTML file in the exact same directory as this __init__.py file
    html_path = os.path.join(os.path.dirname(__file__), "hgase_genomic_crosswalk.html")
    
    # Serve the file directly through ComfyUI
    if os.path.exists(html_path):
        return web.FileResponse(html_path)
    
    return web.Response(text="HGASE Engine HTML not found. Ensure hgase_genomic_crosswalk.html is in the custom_nodes/HGASE_Engine folder.", status=404)

print("[HGASE] Neural Strata Integrated. Access the Genomic Crosswalk at: http://127.0.0.1:8188/hgase")