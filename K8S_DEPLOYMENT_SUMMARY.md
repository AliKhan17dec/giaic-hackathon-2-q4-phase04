# Todo Chat - Local Kubernetes Deployment

## 📁 Files Created

Your local Kubernetes deployment setup is now complete! Here's what was created:

### Helm Chart (`helm/todo-chat/`)
- ✅ `Chart.yaml` - Helm chart metadata
- ✅ `values.yaml` - Default configuration values (with your Gemini API key)
- ✅ `values-local.yaml` - Local-specific values for minikube
- ✅ `README.md` - Helm chart documentation
- ✅ `.helmignore` - Files to exclude from Helm package

### Kubernetes Templates (`helm/todo-chat/templates/`)
- ✅ `_helpers.tpl` - Template helper functions
- ✅  `backend-deployment.yaml` - Backend deployment configuration
- ✅ `backend-service.yaml` - Backend service
- ✅ `frontend-deployment.yaml` - Frontend deployment configuration
- ✅ `frontend-service.yaml` - Frontend service (NodePort for easy access)
- ✅ `postgresql-deployment.yaml` - PostgreSQL database deployment
- ✅ `postgresql-service.yaml` - PostgreSQL service
- ✅ `postgresql-pvc.yaml` - Persistent volume claim for database
- ✅ `configmap.yaml` - Configuration management
- ✅ `secret.yaml` - Secrets management (API keys, passwords)
- ✅ `serviceaccount.yaml` - Service account for pods
- ✅ `ingress.yaml` - Ingress configuration (optional)
- ✅ `NOTES.txt` - Post-installation instructions

### Helper Scripts (Root Directory)
- ✅ `deploy-local.sh` - Complete deployment automation script
- ✅ `build-images.sh` - Build Docker images for minikube
- ✅ `cleanup.sh` - Remove deployment and cleanup resources

### Documentation
- ✅ `DEPLOYMENT.md` - Comprehensive deployment guide
- ✅ `QUICK_REFERENCE.md` - Quick command reference

## 🚀 Quick Start (3 Steps)

### 1. Make sure minikube is running
```bash
minikube status
# If not running:
minikube start --driver=docker --memory=4096 --cpus=2
```

### 2. Run the deployment script
```bash
./deploy-local.sh
```

This script automatically:
- Verifies prerequisites (minikube, helm, kubectl)
- Builds Docker images in minikube's Docker daemon
- Creates the Kubernetes namespace
- Deploys all components with Helm
- Waits for pods to be ready

### 3. Access the application
```bash
minikube service frontend --namespace todo-chat
```

This will open your browser to the frontend application!

## 📊 What Gets Deployed

Your deployment includes:

1. **Frontend (Next.js)**
   - Accessible via NodePort at port 30080
   - 1 replica
   - 300m CPU / 256Mi RAM limits

2. **Backend (FastAPI)**
   - Internal ClusterIP service
   - 1 replica
   - 500m CPU / 512Mi RAM limits
   - Health checks configured

3. **PostgreSQL Database**
   - Persistent storage (1Gi)
   - Internal ClusterIP service
   - Health checks configured
   - Data persists across pod restarts

## 🔧 Configuration

All configuration is in `helm/todo-chat/values.yaml`:

```yaml
backend:
  env:
    DATABASE_URL: "postgresql://postgres:postgres@postgresql:5432/todochat"
    JWT_SECRET: "a-very-secret-key"
    GEMINI_API_KEY: "AIzaSyAv-lXBPDbEjOVlNKWweStuXp0ZYVKXIuU"  # Your key

postgresql:
  auth:
    database: todochat
    username: postgres
    password: postgres  # Change for production!

frontend:
  service:
    nodePort: 30080  # Access at minikube-ip:30080
```

## 📝 Common Commands

```bash
# View all resources
kubectl get all -n todo-chat

# View logs
kubectl logs -n todo-chat -l app.kubernetes.io/component=backend -f
kubectl logs -n todo-chat -l app.kubernetes.io/component=frontend -f
kubectl logs -n todo-chat -l app.kubernetes.io/component=database -f

# Get frontend URL
minikube service frontend --namespace todo-chat --url

# Update deployment
helm upgrade todo-chat ./helm/todo-chat --namespace todo-chat

# Rollback
helm rollback todo-chat --namespace todo-chat

# Uninstall
./cleanup.sh
# or
helm uninstall todo-chat --namespace todo-chat
```

## 🔄 Making Changes

### After Code Changes

```bash
# Rebuild images
./build-images.sh

# Restart pods to use new images
kubectl rollout restart deployment -n todo-chat
```

### After Configuration Changes

```bash
# Edit values
nano helm/todo-chat/values.yaml

# Apply changes
helm upgrade todo-chat ./helm/todo-chat --namespace todo-chat
```

## 🐛 Troubleshooting

### Images not found
```bash
# Make sure you built in minikube's Docker daemon
eval $(minikube docker-env)
./build-images.sh
```

### Pods not starting
```bash
# Check pod status and events
kubectl describe pod -n todo-chat <pod-name>

# Check logs
kubectl logs -n todo-chat <pod-name>
```

### Can't access frontend
```bash
# Get minikube IP
minikube ip

# Get NodePort
kubectl get svc -n todo-chat frontend

# Try port forwarding instead
kubectl port-forward -n todo-chat svc/frontend 3000:3000
# Then access at http://localhost:3000
```

### Database connection errors
```bash
# Check if PostgreSQL is ready
kubectl get pods -n todo-chat | grep postgresql

# Check database logs
kubectl logs -n todo-chat -l app.kubernetes.io/component=database

# Verify database service
kubectl get svc -n todo-chat postgresql
```

## 📚 Next Steps

1. **Test the Application**
   - Sign up for a new account
   - Log in
   - Try chat commands like "add a task to buy milk"

2. **Monitor Resources**
   ```bash
   kubectl top pods -n todo-chat
   minikube dashboard
   ```

3. **Scale if Needed**
   ```bash
   helm upgrade todo-chat ./helm/todo-chat \
     --set backend.replicaCount=2 \
     --set frontend.replicaCount=2 \
     --namespace todo-chat
   ```

4. **Enable Ingress (Optional)**
   ```bash
   helm upgrade todo-chat ./helm/todo-chat \
     --set ingress.enabled=true \
     --namespace todo-chat
   ```

## 🛡️ Security Notes

For **production** deployments, make sure to:

- [ ] Change `JWT_SECRET` to a strong random value
- [ ] Change PostgreSQL password
- [ ] Use external database with backups
- [ ] Enable TLS/HTTPS
- [ ] Set up proper ingress with authentication
- [ ] Configure resource limits based on load testing
- [ ] Use image scanning and vulnerability management
- [ ] Implement network policies

## 📖 Additional Resources

- Full deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- Quick reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- Helm chart README: [helm/todo-chat/README.md](helm/todo-chat/README.md)

---

**Everything is ready! Run `./deploy-local.sh` to get started! 🎉**
