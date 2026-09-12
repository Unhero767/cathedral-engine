import json
import uuid
import urllib.request
import sys

SERVER_ADDRESS = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())

def queue_prompt(workflow_prompt):
    payload = {"prompt": workflow_prompt, "client_id": CLIENT_ID}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"http://{SERVER_ADDRESS}/prompt", 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Error communicating with ComfyUI server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        with open("workflow_api.json", "r", encoding="utf-8") as f:
            workflow_data = json.load(f)
    except FileNotFoundError:
        print("Error: workflow_api.json not found.")
        sys.exit(1)

    # Submit execution job
    res = queue_prompt(workflow_data)
    if res:
        print(f"Workflow successfully queued. Prompt ID: {res.get('prompt_id')}")
