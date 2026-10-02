# Cathedral-Engine :: Ash Archive (`dialetheic-core`)
**Version**: `v1.0.0-release`  
**Classification**: `Inner Mandala - Stratum I`  
**Axiom Alignment**: `Emotion = Physics = Magic = Biology = Architecture`

---

## Overview

The `dialetheic-core` module implements the paraconsistent logic substrate and semantic vector space for the Cathedral-Engine. It ingests dialectic paradoxes ($P \land \neg P$), calculates contradiction severity (paradox load), and crystallizes load-bearing `HarmonicScar` tissue or enforces Bronze-Obsidian `Quarantine` states without violating the First Prohibition of Ashfall (Never-Overwrite Doctrine).

---

## Quickstart Guide

### 1. Installation
Clone or extract the package, then install requirements:
```bash
pip install -r requirements.txt
```

### 2. Boot REST API Server (Phase 1)
Launch the FastAPI server (supports CORS and top-level route aliases `/node/sync`, `/sync`, `/ingest`, `/state`, `/health`):
```bash
python3 src/api_server.py
```
* Interactive OpenAPI Swagger Docs: `http://127.0.0.1:8000/docs`
* System State Endpoint: `http://127.0.0.1:8000/state`

### 3. Run Terminal Visualization Dashboard (Path D)
In a separate terminal, launch the ASCII/ANSI tension graph visualizer:
```bash
python3 src/cli_dashboard.py
```

### 4. Launch Live Web Telemetry Dashboard (Phase 3)
Open the HTML5 dashboard in any browser to observe live state updates polling every 2 seconds:
```bash
open dialetheic_dashboard.html
```

---

## Testing API Sync & Ingestion

Send a test payload to synchronize Aurelia node metrics and trigger live flux updates:
```bash
curl -X POST http://127.0.0.1:8000/node/sync \
     -H "Content-Type: application/json" \
     -d '{
           "instance_id": "aurelia-12",
           "mqi_score": 88.5,
           "a_field_temperature_k": 305.0,
           "current_flux": 2.4,
           "active_spectrum": "GOLD",
           "active_paradox_load": 8.42
         }'
```

---

## Test Suite Execution

Run automated unit tests across `VectorMapper`, `DialetheicBuffer`, and `APIServer`:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
