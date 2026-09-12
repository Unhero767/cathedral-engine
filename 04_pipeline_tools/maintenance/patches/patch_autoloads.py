import os, re, sys

print("\n" + "="*70)
print(" CATHEDRAL-ENGINE GODOT 4.x AUTOLOAD & CLASS AUDIT & REPAIR")
print("="*70 + "\n")

# 1. Locate project.godot and extract Autoloads
autoloads = {}
pg_path = None
for root, _, files in os.walk('.'):
    if 'project.godot' in files:
        pg_path = os.path.join(root, 'project.godot')
        break

if not pg_path:
    print("[-] Notice: project.godot not found in root. Using standard singleton list.")
else:
    print(f"[*] project.godot found at: {pg_path}")
    with open(pg_path, 'r', encoding='utf-8') as f:
        pg_content = f.read()

    autoload_sec = re.search(r'\[autoload\](.*?)(?:\[|\Z)', pg_content, re.DOTALL)
    if autoload_sec:
        for line in autoload_sec.group(1).splitlines():
            m = re.match(r'^\s*([A-Za-z0-9_]+)\s*=\s*\"?\*?res://([^\"]+)\"?', line.strip())
            if m:
                autoloads[m.group(1)] = m.group(2)

    print(f"[*] Registered Autoload Singletons ({len(autoloads)}):")
    for k, v in autoloads.items():
        print(f"    - {k} -> res://{v}")
    print()

# 2. Add standard Cathedral-Engine singletons to the watch list
standard_singletons = [
    'CathedralSync', 'SpectralConstants', 'AFieldManager', 
    'SomaticBaseline', 'TriKeyController', 'OracleDeckManager', 
    'SanguineHeuristics', 'ChamberManager'
]
watch_names = sorted(list(set(list(autoloads.keys()) + standard_singletons)))
pattern = re.compile(rf'^(class_name\s+({"|".join(map(re.escape, watch_names))}))(\s.*)?$', re.MULTILINE)

# 3. Scan and patch all .gd files
audited_files = 0
patched_files = 0
collisions_fixed = 0

for root, _, files in os.walk('.'):
    for f in files:
        if f.endswith('.gd'):
            audited_files += 1
            f_path = os.path.join(root, f)
            with open(f_path, 'r', encoding='utf-8') as gf:
                content = gf.read()
            
            matches = pattern.findall(content)
            if matches:
                # Backup original file
                with open(f_path + '.bak', 'w', encoding='utf-8') as bf:
                    bf.write(content)
                
                # Comment out conflicting class_name
                new_content = pattern.sub(r'# \1\3 # [Patched: Autoload Singleton Compatibility]', content)
                with open(f_path, 'w', encoding='utf-8') as gf:
                    gf.write(new_content)
                
                names_found = [m[1] for m in matches]
                print(f"[+] FIXED: {f_path}")
                print(f"    Commented out class_name: {names_found}")
                patched_files += 1
                collisions_fixed += len(matches)

print("\n" + "-"*70)
print(" AUDIT SUMMARY:")
print(f" - Total .gd files audited     : {audited_files}")
print(f" - Files patched & backed up   : {patched_files}")
print(f" - Total namespace collisions  : {collisions_fixed}")
print("="*70 + "\n")
