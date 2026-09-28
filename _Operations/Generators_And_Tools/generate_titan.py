import json
import urllib.request
import urllib.parse
import time
import os
import random

SERVER_ADDRESS = "127.0.0.1:8188"
WORKFLOW_FILE = "workflow_api.json"
OUTPUT_DIR = "./generated_images"
BATCH_SIZE = 5 # Change this number to generate more or fewer images

os.makedirs(OUTPUT_DIR, exist_ok=True)

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_history(prompt_id):
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/history/{prompt_id}")
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/view?{url_values}")
    return urllib.request.urlopen(req).read()

def main():
    with open(WORKFLOW_FILE, "r") as f:
        workflow = json.load(f)

    print(f">> Initializing M.L.A.O.S. Visual Synthesis (Batch of {BATCH_SIZE})...")
    
    for i in range(1, BATCH_SIZE + 1):
        # Randomize the seed for every new image!
        workflow["3"]["inputs"]["seed"] = random.randint(1, 999999999)
        
        print(f">> Queuing image {i}/{BATCH_SIZE} (Seed: {workflow['3']['inputs']['seed']})...")
        prompt_id = queue_prompt(workflow)['prompt_id']

        while True:
            history = get_history(prompt_id)
            if prompt_id in history:
                break
            time.sleep(1)

        outputs = history[prompt_id]['outputs']
        for node_id in outputs:
            node_output = outputs[node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    save_path = os.path.join(OUTPUT_DIR, image['filename'])
                    with open(save_path, "wb") as f:
                        f.write(image_data)
                    print(f">> Image {i} saved to: {save_path}")

if __name__ == "__main__":
    main()
