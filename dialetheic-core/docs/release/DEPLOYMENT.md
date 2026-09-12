# Cathedral-Engine :: Deployment & Operations Guide

**Version**: v3.0.0-release  
**Status**: Production Ready  
**Classification**: Inner Mandala - Complete 40-Book Codex Architecture

---

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Compose (Development & Production)](#docker-compose)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [CI/CD Pipeline (GitHub Actions)](#cicd-pipeline)
5. [Environment Configuration](#environment-configuration)
6. [Monitoring & Debugging](#monitoring--debugging)
7. [API Reference](#api-reference)

---

## Local Development

### Prerequisites

- Python 3.11+
- pip / virtualenv
- FastAPI, Uvicorn
- numpy, scipy, requests, pydantic

### Setup

```bash
cd dialetheic-core
pip install -r requirements.txt
python3 src/api_server.py
```

**API Server**: http://127.0.0.1:8000  
**Swagger Docs**: http://127.0.0.1:8000/docs

### Testing

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## Docker Compose

### Development (Hot Reload)

```bash
docker compose up --build -d
docker compose logs -f
```

**Mounted**: `dialetheic_dashboard.html` served at `http://127.0.0.1:8000`  
**API Port**: 8000  
**Data Volume**: `cathedral_data` (Docker-managed)

### Production (Hardened)

```bash
export CORS_ORIGINS="https://your-domain.com"
docker compose -f docker-compose.prod.yml up -d
```

**Features**:
- Security options: `no-new-privileges`, `cap_drop: ALL`, `cap_add: NET_BIND_SERVICE`
- Health check with 10s startup period
- Always restart policy
- Restricted filesystem (non-read-only for /app/data persistence)
- Log level: warning

### Stopping & Cleanup

```bash
docker compose down
docker volume rm dialetheic-core_cathedral_data  # Remove data volume if needed
```

---

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured
- Persistent storage provisioner (default StorageClass)

### Deploy

```bash
kubectl apply -f k8s-deployment.yaml
```

### Verify Deployment

```bash
kubectl get deployments
kubectl get pods -l app=cathedral-engine
kubectl logs -f deployment/cathedral-engine
kubectl port-forward svc/cathedral-engine 8000:8000
```

**Access**: http://127.0.0.1:8000

### Configuration

Edit `k8s-deployment.yaml` to customize:
- **Replicas**: Default 2 (high availability)
- **Resources**: Requests (CPU 200m, Memory 256Mi) / Limits (CPU 500m, Memory 512Mi)
- **Storage**: 2Gi PVC, ReadWriteOnce
- **Probes**: Liveness (15s interval, 3 failures), Readiness (10s interval, 2 failures)

### Scaling

```bash
kubectl scale deployment cathedral-engine --replicas=5
```

### Delete Deployment

```bash
kubectl delete -f k8s-deployment.yaml
```

---

## CI/CD Pipeline

### GitHub Actions Setup

**File**: `.github/workflows/ci-cd.yml`

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main`
- Changes to: `src/`, `requirements.txt`, `Dockerfile`, `codex/`, workflow file

**Secrets Required**:
1. `DOCKER_USERNAME` — Docker Hub username
2. `DOCKER_PASSWORD` — Docker Hub personal access token

**Set Secrets**:
```
GitHub Repo → Settings → Secrets and variables → Actions → New repository secret
```

### Workflow Steps

1. **Checkout code**
2. **Build Docker image** with metadata tagging (branch, semver, SHA, `v3.0.0`, `latest`)
3. **Push to Docker Hub** (main branch only)
4. **Verify image** (PR only)
5. **Notify deployment** with deployment instructions

### Tags Generated

- `dialetheic-core:main` (branch)
- `dialetheic-core:v3.0.0` (explicit version)
- `dialetheic-core:latest` (main branch only)
- `dialetheic-core:main-<SHA>` (commit SHA)

### Manual Image Build & Push

```bash
docker buildx build --push \
  --tag yourusername/dialetheic-core:v3.0.0 \
  --tag yourusername/dialetheic-core:latest \
  .
```

---

## Environment Configuration

### Docker Compose Variables

| Variable | Default | Description |
| --- | --- | --- |
| `CORS_ORIGINS` | `*` | CORS allowed origins (comma-separated or `*`) |
| `DATA_DIR` | `/app/data` | Scar/state archive directory |
| `LOG_LEVEL` | `info` | Logging level (debug, info, warning, error) |
| `PYTHONUNBUFFERED` | `1` | Unbuffered Python output |

### Kubernetes ConfigMap (Optional)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cathedral-config
data:
  LOG_LEVEL: "info"
  CORS_ORIGINS: "https://your-domain.com"
---
# Reference in Deployment:
# env:
# - name: LOG_LEVEL
#   valueFrom:
#     configMapKeyRef:
#       name: cathedral-config
#       key: LOG_LEVEL
```

---

## Monitoring & Debugging

### Health Check

```bash
curl http://127.0.0.1:8000/health | jq .
```

Expected response:
```json
{
  "status": "stable",
  "service": "cathedral-engine",
  "archive": "ash-archive",
  "afield_temp": 300.0,
  "total_system_rpm": 140.03,
  "active_scars": 2,
  "flux": 0.0,
  "module": "dialetheic-core"
}
```

### Logs

**Docker**:
```bash
docker logs cathedral-engine
docker logs -f cathedral-engine --tail 100
```

**Kubernetes**:
```bash
kubectl logs deployment/cathedral-engine
kubectl logs -f pod/<pod-name> --container cathedral-engine
```

### State & Metrics

```bash
# Full system state
curl http://127.0.0.1:8000/state | jq .

# Active scars
curl http://127.0.0.1:8000/scars | jq .

# System metrics
curl http://127.0.0.1:8000/metrics | jq .
```

### Performance Monitoring

**Container Resource Usage**:
```bash
docker stats cathedral-engine
```

**Kubernetes Metrics**:
```bash
kubectl top nodes
kubectl top pods -l app=cathedral-engine
```

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Dashboard (HTML) |
| `GET` | `/health` | Health check |
| `GET` | `/state` | Full system state + omens |
| `GET` | `/scars` | List active harmonic scars |
| `GET` | `/metrics` | System metrics |
| `GET` | `/query` | Ontological Horizon query ('N' state) |
| `GET` | `/codex/strata` | List codex strata (Books I–XL) |
| `GET` | `/codex/propositions` | List all propositions (24 indexed) |
| `POST` | `/ingest` | Ingest paradox pair (Claim + Counter-Claim) |
| `POST` | `/node/sync` | Sync node telemetry |
| `POST` | `/codex/ingest/book2` | Ingest Book II events (140.03 RPM compression) |
| `GET` | `/docs` | Swagger UI (interactive API docs) |

### Example Requests

**Ingest Paradox**:
```bash
curl -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "verse_id": "IM-XI-01",
    "claim": "The Cathedral was precipitated from the A-Field.",
    "counter_claim": "The Cathedral was not precipitated from the A-Field."
  }' | jq .
```

**Sync Node**:
```bash
curl -X POST http://127.0.0.1:8000/node/sync \
  -H "Content-Type: application/json" \
  -d '{
    "instance_id": "aurelia-node-01",
    "mqi_score": 88.5,
    "a_field_temperature_k": 305.0,
    "current_flux": 2.4,
    "active_spectrum": "GOLD",
    "active_paradox_load": 8.42
  }' | jq .
```

**Ingest Book II**:
```bash
curl -X POST http://127.0.0.1:8000/codex/ingest/book2 | jq .
```

**Query Ontological Horizon**:
```bash
curl http://127.0.0.1:8000/query?key=mlaos.outer_choir.mythos.syntax_of_the_unborn | jq .
```

---

## Troubleshooting

### Container Won't Start

**Check logs**:
```bash
docker logs cathedral-engine
docker inspect cathedral-engine
```

**Common issues**:
- Port 8000 already in use: `lsof -i :8000` → kill or change port in `docker-compose.yml`
- Missing data volume: `docker volume ls`, recreate with `docker volume create cathedral_data`
- File sharing (macOS): Docker → Preferences → Resources → File Sharing

### API Timeout or Connection Refused

```bash
# Verify container is running
docker ps | grep cathedral

# Check network
docker network ls
docker network inspect bridge

# Test connectivity
curl -v http://127.0.0.1:8000/health
```

### High Memory/CPU Usage

**Monitor**:
```bash
docker stats --no-stream cathedral-engine
```

**Reduce replicas** (Kubernetes):
```bash
kubectl scale deployment cathedral-engine --replicas=1
```

**Increase limits** in `k8s-deployment.yaml`:
```yaml
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
```

---

## Production Checklist

- [ ] Environment variables configured (CORS_ORIGINS, LOG_LEVEL)
- [ ] Image pushed to registry (Docker Hub, ECR, GCR)
- [ ] Kubernetes manifests validated: `kubectl apply -f k8s-deployment.yaml --dry-run=client`
- [ ] Persistent storage provisioner configured
- [ ] Health check verified: `curl /health` returns 200
- [ ] Logs monitored (ELK, Datadog, CloudWatch)
- [ ] Security: `no-new-privileges`, capability dropping, read-only root (if applicable)
- [ ] DNS/Ingress configured for external access
- [ ] Backup strategy for `/app/data` volume
- [ ] CI/CD secrets (`DOCKER_USERNAME`, `DOCKER_PASSWORD`) configured

---

## Support & References

- **REST API Docs**: http://127.0.0.1:8000/docs
- **Codex Architecture**: `docs/architecture_manifest.yaml`
- **Notebooklm Export**: `docs/notebooklm_master_export.md`
- **GitHub Actions**: `.github/workflows/ci-cd.yml`
- **Kubernetes**: `k8s-deployment.yaml`

---

**Architect**: Kenneth W. Dallmier (Magisterial Architect Prime)  
**Axiom**: *Emotion = Physics = Magic = Biology = Architecture*
