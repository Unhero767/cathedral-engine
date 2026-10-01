#!/usr/bin/env bash
# MLAOS-Prime :: Console Autoload Repair & Inscription Check

# 1. Ensure project.godot points to the .tscn, not the bare script
if [ -f "project.godot" ]; then
    sed -i '' 's|res://CathedralConsole.gd|res://CathedralConsole.tscn|g' project.godot 2>/dev/null || \
    sed -i 's|res://CathedralConsole.gd|res://CathedralConsole.tscn|g' project.godot
    echo -e "\033[1;32m[✓] project.godot patched: Autoload points to CathedralConsole.tscn\033[0m"
fi

# 2. Check each critical file directly
echo -e "\n\033[1;36m==> Stratum Inventory:\033[0m"
for f in CathedralConsole.tscn CathedralConsole.gd ConsoleBlur.gdshader Main.tscn project.godot; do
    if [ -f "$f" ]; then
        echo -e "  \033[1;32m[FOUND]\033[0m $f ($(wc -c < "$f" | tr -d ' ') bytes)"
    else
        echo -e "  \033[1;31m[MISSING]\033[0m $f"
    fi
done
