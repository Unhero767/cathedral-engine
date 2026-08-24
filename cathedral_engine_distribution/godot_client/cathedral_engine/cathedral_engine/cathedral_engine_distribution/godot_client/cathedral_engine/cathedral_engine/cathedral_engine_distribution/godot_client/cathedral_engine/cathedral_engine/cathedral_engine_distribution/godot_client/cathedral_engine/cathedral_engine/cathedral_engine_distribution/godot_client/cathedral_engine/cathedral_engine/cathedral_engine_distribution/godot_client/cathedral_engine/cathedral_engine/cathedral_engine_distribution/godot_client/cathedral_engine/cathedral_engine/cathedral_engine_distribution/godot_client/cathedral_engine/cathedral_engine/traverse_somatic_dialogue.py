import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:5050/api/rpg"

def get(endpoint, params):
    url = f"{BASE_URL}/{endpoint}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "CathedralCLI/1.0"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

def traverse_tree(tree_name, initial_node="start"):
    print("==================================================")
    print(f" TRAVERSING DIALOGUE TREE: {tree_name}")
    print("==================================================")
    
    current_node = initial_node
    step = 1

    while current_node:
        print(f"\n--- [STEP {step}] Querying Node: '{current_node}' ---")
        res = get("dialogue", {"tree": tree_name, "node": current_node})
        
        # Fallback to 'start' if initial custom node is not directly indexed
        if "error" in res and current_node != "start":
            print(f"[-] Node '{current_node}' not found. Falling back to root 'start' node...")
            current_node = "start"
            res = get("dialogue", {"tree": tree_name, "node": current_node})
            
        if "error" in res:
            print(f"[-] Dialogue error: {res}")
            break

        node_data = res.get("node", {})
        speaker = node_data.get("speaker", "Unknown")
        spec = node_data.get("speaker_spectrum", "Teal")
        text = node_data.get("text", "")
        options = node_data.get("options", [])

        print(f"► Speaker: {speaker} [{spec}]")
        print(f"  \"{text}\"")

        if not options:
            print("\n★ Terminal Leaf Node reached. Dialogue sequence resolved.")
            break

        print("\nAvailable Choices:")
        for idx, opt in enumerate(options):
            label = opt.get("text", "")
            req_spec = opt.get("spectral_requirement", "None")
            print(f"  [{idx}] {label} (Spectral Req: {req_spec})")

        # Execute Choice 0
        print("\nExecuting Choice [0]...")
        choice_res = get("dialogue_choice", {
            "tree": tree_name,
            "node": current_node,
            "choice": 0
        })

        reward = choice_res.get("insight_reward", 0)
        ledger_hash = choice_res.get("ledger_hash", "NONE")
        print(f"  └─ Insight Awarded: +{reward} | Ledger Ref: {ledger_hash[:16]}...")

        # Extract next node target safely
        next_obj = choice_res.get("next_node")
        if isinstance(next_obj, dict):
            current_node = next_obj.get("node_id")
        elif isinstance(next_obj, str):
            current_node = next_obj
        else:
            current_node = None

        step += 1

traverse_tree("CHAMBER_II_SOMATIC", initial_node="cryo_line_regulation")
