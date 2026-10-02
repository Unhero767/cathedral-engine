#!/usr/bin/env bash
set -euo pipefail
WORKSPACE_PATH="/users/kennethdallmier/cathedral_engine"
cd "$WORKSPACE_PATH"

echo "[LIVE WORKSPACE] Spawning split-pane Cathedral session..."

# Launch kitty with a side-by-side split layout
kitty --title "Cathedral Engine | Active Workspace" --directory "$WORKSPACE_PATH" \
      sh -c "./cathedral_deck.sh" \
      --hold &

sleep 0.5
echo "[LIVE WORKSPACE] Session active."
