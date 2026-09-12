import json
import urllib.request
import urllib.parse
import websocket
import uuid
import os
import requests

SERVER_ADDRESS = "127.0.0.1:8181"  # Adjust if your ComfyUI runs on a different port
CLIENT_ID = str(uuid.uuid4())

def queue_prompt(workflow_json):
    """Sends the workflow JSON to the ComfyUI API prompt endpoint."""
    data = {"prompt": workflow_json, "client_id": CLIENT_ID}
    req = urllib.request.Request(
        f"http://{SERVER_ADDRESS}/prompt",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    response = urllib.request.urlopen(req)
    return json.loads(response.read())

def get_image(filename, subfolder, folder_type):
    """Downloads the generated output image from ComfyUI."""
    params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(params)
    response = requests.get(f"http://{SERVER_ADDRESS}/view?{url_values}")
    return response.content

def get_history(prompt_id):
    """Retrieves execution history and output metadata for a completed prompt."""
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def main():
    workflow_path = "workflow_api.json"
    
    if not os.path.exists(workflow_path):
        print(f"Error: Workflow file not found at '{workflow_path}'.")
        print("Tip: In ComfyUI, enable 'Save (API Format)' in settings and save your workflow.")
        return

    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow_data = json.load(f)

    ws = websocket.WebSocket()
    ws.connect(f"ws://{SERVER_ADDRESS}/ws?clientId={CLIENT_ID}")

    print(f"Submitting workflow to ComfyUI at {SERVER_ADDRESS}...")
    response = queue_prompt(workflow_data)
    prompt_id = response['prompt_id']
    print(f"Prompt queued successfully. ID: {prompt_id}")

    output_images = {}
    
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break
                elif data['node']:
                    print(f"Executing node: {data['node']}")
        else:
            continue

    ws.close()

    history = get_history(prompt_id)[prompt_id]
    os.makedirs("comfy_outputs", exist_ok=True)
    
    for node_id, node_output in history['outputs'].items():
        if 'images' in node_output:
            output_images[node_id] = []
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                output_path = os.path.join("comfy_outputs", image['filename'])
                with open(output_path, "wb") as img_file:
                    img_file.write(image_data)
                print(f"Saved generated asset: {output_path}")

if __name__ == "__main__":
    main()
