# Todo Chart - Quick Reference

## Quick Start

```bash
# 1. Build and deploy everything
./deploy-local.sh

# 2. Access the application
minikube service frontend --namespace todo-chat
```

## Common Commands

### Build Images
```bash
./build-images.sh
```

### Deploy
```bash
# Deploy with default values
helm install todo-chat ./helm/todo-chat --namespace todo-chat

# Deploy with local values (includes actual Gemini API key)
helm install todo-chat ./helm/todo-chat -f helm/todo-chat/values-local.yaml --namespace todo-chat

# Upgrade existing deployment
helm upgrade todo-chat ./helm/todo-chat --namespace todo-chat
```

### Access Application
```bash
# Get frontend URL
minikube service frontend --namespace todo-chat --url

# Open frontend in browser
minikube service frontend --namespace todo-chat

# Port forward backend
kubectl port-forward -n todo-chat svc/backend 8000:8000
# Access at http://localhost:8000/docs
```

### View Logs
```bash
# Backend logs
kubectl logs -n todo-chat -l app.kubernetes.io/component=backend -f

# Frontend logs
kubectl logs -n todo-chat -l app.kubernetes.io/component=frontend -f

# Database logs
kubectl logs -n todo-chat -l app.kubernetes.io/component=database -f

# All logs
kubectl logs -n todo-chat --all-containers=true -f
```

### Check Status
```bash
# View all resources
kubectl get all -n todo-chat

# View pods
kubectl get pods -n todo-chat

# View services
kubectl get svc -n todo-chat

# View persistent volumes
kubectl get pvc -n todo-chat

# Describe a pod
kubectl describe pod -n todo-chat <pod-name>
```

### Troubleshooting
```bash
# Check pod events
kubectl get events -n todo-chat --sort-by='.lastTimestamp'

# Execute command in pod
kubectl exec -it -n todo-chat <pod-name> -- /bin/sh

# Check resource usage
kubectl top pods -n todo-chat

# Restart deployment
kubectl rollout restart deployment -n todo-chat
```

### Cleanup
```bash
# Run cleanup script
./cleanup.sh

# Manual cleanup
helm uninstall todo-chat --namespace todo-chat
kubectl delete namespace todo-chat
```

## Minikube Commands

```bash
# Start minikube
minikube start --driver=docker --memory=4096 --cpus=2

# Stop minikube
minikube stop

# Delete minikube
minikube delete

# Get minikube IP
minikube ip

# Use minikube's Docker daemon
eval $(minikube docker-env)

# SSH into minikube
minikube ssh

# Open Kubernetes dashboard
minikube dashboard
```

## Helm Commands

```bash
# List releases
helm list -n todo-chat

# Get values
helm get values todo-chat -n todo-chat

# Get manifest
helm get manifest todo-chat -n todo-chat

# History
helm history todo-chat -n todo-chat

# Rollback
helm rollback todo-chat -n todo-chat

# Uninstall
helm uninstall todo-chat -n todo-chat
```

## Configuration

### Update Gemini API Key
```bash
# Edit values file
nano helm/todo-chat/values.yaml
# or
nano helm/todo-chat/values-local.yaml

# Update deployment
helm upgrade todo-chat ./helm/todo-chat --namespace todo-chat
```

### Update Environment Variables
```bash
# Edit secret
kubectl edit secret -n todo-chat todo-chat-secret

# Or update via Helm values and upgrade
helm upgrade todo-chat ./helm/todo-chat --namespace todo-chat
```

## Database Access

```bash
# Port forward to PostgreSQL
kubectl port-forward -n todo-chat svc/postgresql 5432:5432

# Connect with psql
psql postgresql://postgres:postgres@localhost:5432/todochat

# Execute command in PostgreSQL pod
kubectl exec -it -n todo-chat deployment/todo-chat-postgresql -- psql -U postgres -d todochat
```

## Tips

1. **Build images in minikube's Docker daemon:**
   ```bash
   eval $(minikube docker-env)
   ```

2. **Quick redeploy after code changes:**
   ```bash
   ./build-images.sh && kubectl rollout restart deployment -n todo-chat
   ```

3. **Watch pod status:**
   ```bash
   watch kubectl get pods -n todo-chat
   ```

4. **Get all pod logs:**
   ```bash
   kubectl logs -n todo-chat --all-containers=true --tail=100
   ```

5. **Check if images are in minikube:**
   ```bash
   minikube image ls | grep todo-chat
   ```
