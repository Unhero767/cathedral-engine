#!/bin/bash
echo "[CATHEDRAL-ENGINE]: Initializing full-stack simulation runtime..."

# 1. Start Ash Archive Character Stable Ledger (Port 8000)
echo "[STARTING]: Ash Archive Ledger on Port 8000..."
python ash_archive_stable.py &
LEDGER_PID=$!

# 2. Start IPC Spatial Stream Broadcaster (Port 8001)
echo "[STARTING]: IPC Spatial Stream on Port 8001..."
python ipc_spatial_stream.py &
IPC_PID=$!

# 3. Verify Native Llama Matrix (Port 9932)
echo "[VERIFYING]: Native Llama Inference Server on Port 9932..."
if lsof -i :9932 > /dev/null; then
    echo "[STATUS]: Llama matrix online."
else
    echo "[WARNING]: Port 9932 inactive. Igniting llama-server..."
    /Users/kennethdallmier/.llama-app/llama serve \
      --model models/qwen2.5-0.5b.gguf \
      --port 9932 \
      --ctx-size 2048 \
      --log-file /tmp/llama-server.log &
fi

echo ""
echo "[SUCCESS]: Backend strata active. Launching Godot 4 simulation..."
echo "------------------------------------------------------------------"
echo "To terminate all backend services, run: kill $LEDGER_PID $IPC_PID"

# Attempt to launch Godot if executable is in path, or instruct operator
if command -v godot &> /dev/null; then
    godot --path . &
elif [ -d "/Applications/Godot.app" ]; then
    /Applications/Godot.app/Contents/MacOS/Godot --path . &
else
    echo "[NOTICE]: Godot binary not found in standard path. Open Godot 4 manually and load this directory."
fi
