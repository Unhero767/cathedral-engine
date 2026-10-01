#!/usr/bin/env bash
# ====================================================================
# MLAOS-Prime :: Dual-Process Ignition (FastAPI Backend + Godot Engine)
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
set -e

echo "[i] Purging orphaned paraconsistent processes on Port 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

echo "[i] Booting MLAOS-Prime Paraconsistent Backend (Port 8000)..."
studio run-api &
API_PID=$!

sleep 2

echo "[i] Igniting Cathedral-Engine Godot 4 Client..."
studio run-engine

# When Godot closes, terminate the backend server safely
kill -9 $API_PID 2>/dev/null || true
echo "[✓] Continuum disconnected cleanly."
