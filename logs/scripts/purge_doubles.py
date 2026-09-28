import os

DUPLICATES_TO_PURGE = [
    "sercer.py",
    "cathedral_engine_complete.py",
    "run_mlaose.py",
    "Architecting Seamless Navigation in Vanilla JS RPGs_ A Strategy for Hardcoded Bidirectional Linking Using the History API and State Management (1).pdf"
]

def purge_files():
    print("[Purge Utility] Initialized cleanup of redundant double artifacts...")
    for filename in DUPLICATES_TO_PURGE:
        target_path = os.path.join("/users/kennethdallmier/cathedral_engine", filename)
        if os.path.exists(target_path):
            os.remove(target_path)
            print(f"[Removed] Purged duplicate artifact: {filename}")
        else:
            print(f"[Skipped] Target not found: {filename}")
    print("[Purge Utility] Cleanup complete.")

if __name__ == "__main__":
    purge_files()
