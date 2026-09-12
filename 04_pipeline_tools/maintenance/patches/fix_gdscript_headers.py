import os, re

def clean_script_header(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    lines = content.splitlines()
    class_name = None
    extends_class = None
    other_lines = []
    
    for line in lines:
        s = line.strip()
        if s.startswith('class_name '):
            m = re.match(r'^class_name\s+([A-Za-z0-9_]+)(?:\s+extends\s+([A-Za-z0-9_]+))?', s)
            if m:
                class_name = m.group(1)
                if m.group(2):
                    extends_class = m.group(2)
        elif s.startswith('extends '):
            m = re.match(r'^extends\s+([A-Za-z0-9_]+)', s)
            if m and not extends_class:
                extends_class = m.group(1)
        elif s.startswith('# [Patched:') or s.startswith('# class_name'):
            other_lines.append(line)
        else:
            other_lines.append(line)
            
    header = []
    if class_name:
        header.append(f"class_name {class_name}")
    if extends_class:
        header.append(f"extends {extends_class}")
        
    while other_lines and not other_lines[0].strip():
        other_lines.pop(0)
        
    new_content = "\n".join(header) + "\n\n" + "\n".join(other_lines) + "\n"
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[✓] Normalized header in: {file_path}")

for root, _, files in os.walk('.'):
    for f in files:
        if f.endswith('.gd'):
            clean_script_header(os.path.join(root, f))

print("\n[✓] Header audit and normalization complete.")
