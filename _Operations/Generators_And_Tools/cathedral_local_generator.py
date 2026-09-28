import json
import urllib.request

SERVER_ADDRESS = "127.0.0.1:8188"

def queue_workflow(api_json_path):
    with open(api_json_path, "r") as f:
        workflow_data = json.load(f)
    
    payload = {"prompt": workflow_data}
    data = json.dumps(payload).encode("utf-8")
    
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            print(f"[SUCCESS] Workflow queued successfully! Prompt ID: {res.get('prompt_id')}")
    except Exception as e:
        print(f"[ERROR] Could not queue workflow: {e}")

if __name__ == "__main__":
    queue_workflow("workflow_api.json")
