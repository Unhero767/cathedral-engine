#!/usr/bin/env bash
# MLAOS-Prime :: Stratum Verification Utility
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)

FILES=(
    "CathedralConsole.tscn"
    "CathedralConsole.gd"
    "ConsoleBlur.gdshader"
    "project.godot"
)

echo -e "\033[1;36m┌────────────────────────────────────────┐\033[0m"
echo -e "\033[1;36m│   Σ-7 :: VERIFYING FILE INSCRIPTIONS   │\033[0m"
echo -e "\033[1;36m└────────────────────────────────────────┘\033[0m"

for TARGET in "${FILES[@]}"; do
    if [ -f "$TARGET" ]; then
        SIZE=$(wc -c < "$TARGET" | tr -d ' ')
        echo -e "\033[1;32m[+] $TARGET \033[0m($SIZE bytes)"
    else
        echo -e "\033[1;31m[-] $TARGET (NOT FOUND)\033[0m"
    fi
done

echo -e "\n\033[1;33m[i] You can also manually list files by typing:\033[0m"
echo "    ls -lah CathedralConsole.*"
echo "    fd . # If you installed fd in Phase 1"
