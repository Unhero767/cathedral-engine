# Asset 6: Cathedral-Engine Technical CLI & Service Manual
**Version**: `v2.5.0-release`

---

## 1. REST API Server Execution
Start FastAPI server natively:
```bash
python3 src/api_server.py
```

## 2. Interactive Terminal Shell (REPL)
Launch interactive shell:
```bash
python3 src/interactive_shell.py
```

## 3. Automated Batch Codex Ingester
Ingest all JSON codex files in `codex/` directory:
```bash
python3 src/ingest_codex_batch.py
```

## 4. Benchmark Execution
Run VectorMapper benchmark script:
```bash
python3 scripts/benchmark_vector_mapper.py
```
