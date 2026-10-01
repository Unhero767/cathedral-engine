#!/usr/bin/env bash
# ====================================================================
# MLAOS-Prime :: Console Node Path Alignment
# ====================================================================

# Update the OutputLog path to account for the MarginContainer wrapper
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' 's|PanelContainer/VBoxContainer/OutputLog|PanelContainer/VBoxContainer/MarginContainer/OutputLog|g' CathedralConsole.gd
else
    sed -i 's|PanelContainer/VBoxContainer/OutputLog|PanelContainer/VBoxContainer/MarginContainer/OutputLog|g' CathedralConsole.gd
fi

echo -e "\033[1;32m[✓] CathedralConsole.gd paths aligned with scene tree.\033[0m"
