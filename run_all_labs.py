import subprocess

def run_all():
    labs = [
        "experiments/mlaos_scientific_lab.py",
        "experiments/mlaos_graphics_lab.py",
        "experiments/mlaos_arbiter_reconciliation.py",
        "experiments/mlaos_semantic_survival.py",
        "experiments/cathedral_avatar_engine.py",
        "experiments/mlaos_shader_registry.py"
    ]
    print("[CATHEDRAL ENGINE] Executing Master Laboratory Suite...\n" + "="*60)
    for lab in labs:
        print(f"-> Launching Substrate: {lab}")
        res = subprocess.run(["python3", lab], capture_output=True, text=True)
        if res.returncode == 0:
            print(res.stdout.strip())
            print("-> [SUCCESS] Substrate committed.\n" + "-"*40)
        else:
            print(f"-> [ERROR] {res.stderr.strip()}\n" + "-"*40)
    print("="*60)
    print("[CATHEDRAL ENGINE] All subsystems synchronized to Ash Archive.")

if __name__ == "__main__":
    run_all()
