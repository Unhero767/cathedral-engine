#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_PATH="/users/kennethdallmier/cathedral_engine"
cd "$WORKSPACE_PATH"

while true; do
    clear
    echo "=========================================================="
    echo "       CATHEDRAL-ENGINE // COMMAND DECK (MLAOS-PRIME)     "
    echo "=========================================================="
    echo " [1] Inspect Master Avatar Atlas (icat)"
    echo " [2] Inspect Cathedral Concept Art (icat)"
    echo " [3] Run Magisterial Arbiter Reconciliation"
    echo " [4] Boot FastAPI Telemetry Stream"
    echo " [5] Run Matrix Optimization Solver"
    echo " [6] Trigger ComfyUI Asset Generation"
    echo " [7] Exit Control Deck"
    echo "=========================================================="
    read -p "Select operational protocol [1-7]: " choice

    case $choice in
        1)
            echo "[DECK] Rendering master atlas strip..."
            kitty +kitten icat ./assets/portraits/master_atlas_strip.png
            read -p "Press [Enter] to return to deck..."
            ;;
        2)
            echo "[DECK] Rendering cathedral concept art..."
            kitty +kitten icat ./assets/generated/MLAOS_Cathedral_00001_.png
            read -p "Press [Enter] to return to deck..."
            ;;
        3)
            echo "[DECK] Executing Magisterial Arbiter reconciliation..."
            python3 mlaos_arbiter_reconciliation.py
            read -p "Press [Enter] to return to deck..."
            ;;
        4)
            echo "[DECK] Launching FastAPI telemetry service on port 8000..."
            python3 mlaos_telemetry_service.py
            ;;
        5)
            echo "[DECK] Executing matrix optimization sequence..."
            python3 -c '
import numpy as np
A = np.zeros((5, 5))
def add_edge(m, i, j, w):
    res = m.copy()
    res[i, j] = w
    return res
def mu2(m): return m.sum()
best = max(((mu2(add_edge(A, i, j, 0.075)), (i, j)) for i in range(A.shape[0]) for j in range(i + 1, A.shape[0])),)
print("   Optimal Injection Result:", best)
'
            read -p "Press [Enter] to return to deck..."
            ;;
        6)
            echo "[DECK] Enter asset generation prompt:"
            read -p "> " user_prompt
            python3 mlaos_comfy_trigger.py "$user_prompt"
            read -p "Press [Enter] to return to deck..."
            ;;
        7)
            echo "[DECK] Disengaging control deck. Safe travels, Architect."
            exit 0
            ;;
        *)
            echo "[DECK] Unknown protocol selector."
            sleep 1
            ;;
    esac
done
