import os

def print_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        if '.git' in root or '__pycache__' in root:
            continue
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in sorted(files):
            if not f.endswith('.pyc'):
                print(f"{subindent}{f}")

if __name__ == "__main__":
    print("=== DIALETHEIC-CORE DIRECTORY SCAFFOLDING ===")
    print_tree("/working_dir/c_827c0b1127824eba/dialetheic-core")
