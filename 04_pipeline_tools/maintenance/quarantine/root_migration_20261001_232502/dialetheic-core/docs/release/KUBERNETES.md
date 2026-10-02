# Kubernetes Deployment Guide — Cathedral-Engine v3.0.0 Ultra-Interactive

**Classification**: Production Ready  
**Image**: `herounhero/dialetheic-core:v3.0.0-ultra-interactive`  
**Status**: Pushed to Docker Hub

---

## Prerequisites

- Kubernetes cluster v1.24+
- `kubectl` configured and authenticated
- Persistent storage provisioner (default StorageClass)
- Optional: NGINX Ingress Controller + cert-manager for TLS

---

## Quick Start Deployment

### 1. Apply Base Manifests

```bash
# Deploy core resources (Deployment, Service, ConfigMap, PVC, HPA)
kubectl apply -f k8s-deployment.yaml

# Verify deployment
kubectl get pods -l app=cathedral-engine
kubectl get svc cathedral-engine
```

**Expected Output:**
```
NAME                               READY   STATUS    RESTARTS   AGE
cathedral-engine-7f8d9c4b5-abc12   1/1     Running   0          10s
cathedral-engine-7f8d9c4b5-def34   1/1     Running   0          10s
cathedral-engine-7f8d9c4b5-ghi56   1/1     Running   0          10s

NAME                TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)        AGE
cathedral-engine    LoadBalancer   10.0.123.45    203.0.113.50    80:30123/TCP   10s
```

### 2. Test Connectivity

```bash
# Get external IP
kubectl get svc cathedral-engine -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# Test health endpoint
curl http://<EXTERNAL_IP>/health
```

### 3. (Optional) Deploy with Ingress

For HTTPS and domain-based access:

```bash
# Install NGINX Ingress Controller (if not present)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.5.1/deploy/static/provider/cloud/deploy.yaml

# Install cert-manager (if not present)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml

# Update ingress hostname and apply
sed 's/cathedral.example.com/your-domain.com/g' k8s-ingress.yaml | kubectl apply -f -

# Verify ingress
kubectl get ingress cathedral-engine-ingress
```

---

## Configuration

### Environment Variables

Edit `k8s-deployment.yaml` ConfigMap section:

```yaml
data:
  cors_origins: "*"           # CORS allowed origins
  log_level: "info"           # Logging level: debug, info, warning, error
```

Then reapply:
```bash
kubectl apply -f k8s-deployment.yaml
```

### Scaling

#### Manual Scaling

```bash
kubectl scale deployment cathedral-engine --replicas=5
```

#### Automatic Scaling (HPA)

HPA is included in manifests. It scales based on:
- **CPU**: 70% utilization threshold
- **Memory**: 80% utilization threshold
- **Min Replicas**: 3
- **Max Replicas**: 10

Check HPA status:
```bash
kubectl get hpa cathedral-engine-hpa
kubectl describe hpa cathedral-engine-hpa
```

---

## Monitoring & Debugging

### Logs

```bash
# All pods
kubectl logs -l app=cathedral-engine --all-containers=true -f

# Specific pod
kubectl logs -f pod/cathedral-engine-7f8d9c4b5-abc12

# Last 50 lines
kubectl logs -l app=cathedral-engine --tail=50
```

### Pod Status

```bash
# Detailed pod info
kubectl describe pod cathedral-engine-7f8d9c4b5-abc12

# Events (last 10)
kubectl get events -l app=cathedral-engine --sort-by='.lastTimestamp' | tail -10
```

### Resource Usage

```bash
# Real-time metrics
kubectl top pods -l app=cathedral-engine
kubectl top nodes

# Persistent volume usage
kubectl describe pvc cathedral-data-pvc
```

### Access Pod Shell

```bash
kubectl exec -it pod/cathedral-engine-7f8d9c4b5-abc12 -- /bin/bash
```

---

## Advanced Configuration

### Resource Limits Adjustment

Edit `k8s-deployment.yaml`:

```yaml
resources:
  requests:
    cpu: 500m          # Minimum CPU requested
    memory: 1Gi        # Minimum memory requested
  limits:
    cpu: 2000m         # Maximum CPU allowed
    memory: 2Gi        # Maximum memory allowed
```

Apply changes:
```bash
kubectl set resources deployment cathedral-engine \
  --requests=cpu=500m,memory=1Gi \
  --limits=cpu=2000m,memory=2Gi
```

### Pod Anti-Affinity

By default, pods are scheduled on different nodes (preferred). To enforce strict anti-affinity:

```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:  # Change from 'preferred' to 'required'
    - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - cathedral-engine
      topologyKey: kubernetes.io/hostname
```

### Custom Namespace

Deploy in a dedicated namespace:

```bash
kubectl create namespace cathedral
kubectl apply -f k8s-deployment.yaml -n cathedral
```

Update service hostname in your app:
```
http://cathedral-engine.cathedral.svc.cluster.local:8000
```

---

## Health Checks & Probes

### Liveness Probe (Restart Failed Pods)
- **Path**: `/health`
- **Interval**: 20s
- **Timeout**: 5s
- **Failure Threshold**: 3 consecutive failures → pod restart

### Readiness Probe (Traffic Routing)
- **Path**: `/health`
- **Interval**: 10s
- **Timeout**: 3s
- **Failure Threshold**: 2 consecutive failures → pod removed from service endpoints

---

## Troubleshooting

### Pod Stuck in Pending

```bash
kubectl describe pod <pod-name>
# Common causes:
# - Insufficient resources (CPU/memory)
# - PVC not bound (check StorageClass)
# - Node affinity conflicts
```

**Fix:**
```bash
# Check available nodes
kubectl get nodes -o wide

# Check PVC status
kubectl describe pvc cathedral-data-pvc

# Check StorageClass
kubectl get storageclass
```

### CrashLoopBackOff

```bash
kubectl logs <pod-name> --previous
# Check for: missing env vars, API connection errors, module import failures
```

**Fix:**
```bash
kubectl set env deployment cathedral-engine DATA_DIR=/app/data
kubectl rollout restart deployment cathedral-engine
```

### High CPU/Memory Usage

```bash
kubectl top pod <pod-name> --containers
```

**Options:**
1. Increase resource limits
2. Reduce replica count and let HPA scale later
3. Profile application code for bottlenecks

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints cathedral-engine

# Test from another pod
kubectl run -it debug --image=curlimages/curl --rm -- sh
# Inside pod: curl http://cathedral-engine:8000/health
```

---

## Backup & Disaster Recovery

### Backup PVC Data

```bash
# Create snapshot of PVC
kubectl exec -it pod/cathedral-engine-7f8d9c4b5-abc12 -- tar -czf /tmp/data-backup.tar.gz /app/data

# Copy from pod
kubectl cp cathedral-engine-7f8d9c4b5-abc12:/tmp/data-backup.tar.gz ./data-backup.tar.gz
```

### Restore from Backup

```bash
# Create new PVC, mount to pod
# Copy data back
kubectl cp ./data-backup.tar.gz cathedral-engine-7f8d9c4b5-abc12:/tmp/

# Extract
kubectl exec -it pod/cathedral-engine-7f8d9c4b5-abc12 -- tar -xzf /tmp/data-backup.tar.gz -C /
```

---

## Rollout & Updates

### Update Image

```bash
kubectl set image deployment/cathedral-engine \
  cathedral-engine=herounhero/dialetheic-core:v3.0.0-ultra-interactive
```

### Rolling Restart

```bash
kubectl rollout restart deployment/cathedral-engine
```

### Check Rollout Status

```bash
kubectl rollout status deployment/cathedral-engine
```

### Rollback to Previous Version

```bash
kubectl rollout undo deployment/cathedral-engine
```

---

## Cleanup

### Remove Deployment

```bash
# Delete all resources from manifest
kubectl delete -f k8s-deployment.yaml

# Delete PVC (data is lost)
kubectl delete pvc cathedral-data-pvc

# Delete namespace (if custom)
kubectl delete namespace cathedral
```

---

## Production Checklist

- [ ] Image pushed to Docker Hub: `herounhero/dialetheic-core:v3.0.0-ultra-interactive`
- [ ] ConfigMap configured (CORS_ORIGINS, LOG_LEVEL)
- [ ] PVC size appropriate for expected data volume
- [ ] Resource requests/limits tuned for cluster capacity
- [ ] HPA min/max replicas reviewed
- [ ] Health check endpoints working (`/health`)
- [ ] Ingress configured for HTTPS (if needed)
- [ ] Monitoring/logging enabled (Prometheus, ELK, etc.)
- [ ] Backup strategy in place
- [ ] Runbooks documented for common issues
- [ ] Load testing performed
- [ ] Disaster recovery plan tested

---

## API Reference

All endpoints accessible via service:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/` | GET | WebGL 3D Dashboard (HTML) |
| `/health` | GET | Health check |
| `/state` | GET | Full system state + omens |
| `/scars` | GET | List active harmonic scars |
| `/metrics` | GET | System metrics |
| `/query` | GET/POST | Ontological Horizon ('N' state) |
| `/codex/strata` | GET | List codex strata |
| `/codex/propositions` | GET | List all propositions |
| `/ingest` | POST | Ingest paradox pair |
| `/node/sync` | POST | Sync node telemetry |
| `/codex/ingest/book2` | POST | Ingest Book II (140.03 RPM) |
| `/docs` | GET | Swagger UI |

---

## Support & References

- **Docker Image**: `herounhero/dialetheic-core:v3.0.0-ultra-interactive`
- **Local Manifests**: `k8s-deployment.yaml`, `k8s-ingress.yaml`
- **Kubernetes Docs**: https://kubernetes.io/docs/
- **Helm Alternative**: See `README.md` for Helm chart deployment

---

**Architect**: Kenneth W. Dallmier (Magisterial Architect Prime)  
**Axiom**: *Emotion = Physics = Magic = Biology = Architecture*
