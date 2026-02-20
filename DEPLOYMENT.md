# Todo Chat - Local Deployment Guide

Complete guide for deploying the Todo Chat application locally using Kubernetes (minikube) and Helm.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed and running
- [Kubectl](https://kubernetes.io/docs/tasks/tools/) installed
- [Helm](https://helm.sh/docs/intro/install/) installed (v3+)
- Gemini API Key from Google AI Studio

## Project Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Kubernetes Cluster                │
│                                                     │
│  ┌──────────────┐     ┌──────────────┐            │
│  │   Frontend   │────▶│   Backend    │            │
│  │   (Next.js)  │     │  (FastAPI)   │            │
│  │   Port: 3000 │     │  Port: 8000  │            │
│  └──────────────┘     └──────┬───────┘            │
│         │                     │                    │
│         │                     ▼                    │
│         │            ┌──────────────┐             │
│         │            │  PostgreSQL  │             │
│         │            │  Port: 5432  │             │
│         │            └──────────────┘             │
│         │                                          │
│         ▼                                          │
│    NodePort:30080                                  │
└─────────────────────────────────────────────────────┘
```

## Step 1: Start Minikube

```bash
# Start minikube
minikube start --driver=docker --memory=4096 --cpus=2

# Verify minikube is running
minikube status

# Enable necessary addons
minikube addons enable ingress
minikube addons enable metrics-server
```

## Step 2: Build Docker Images

Build the Docker images and load them into minikube's Docker daemon.

### Option A: Build directly in Minikube's Docker daemon

```bash
# Point your shell to minikube's docker daemon
eval $(minikube docker-env)

# Build backend image
cd backend
docker build -t todo-chat-backend:latest .

# Build frontend image
cd ../frontend
docker build -t todo-chat-frontend:latest .

# Verify images are available
docker images | grep todo-chat
```

### Option B: Build and load images

```bash
# Build backend image
cd backend
docker build -t todo-chat-backend:latest .

# Build frontend image
cd ../frontend
docker build -t todo-chat-frontend:latest .

# Load images into minikube
minikube image load todo-chat-backend:latest
minikube image load todo-chat-frontend:latest

# Verify images are available in minikube
minikube image ls | grep todo-chat
```

## Step 3: Configure the Application

Edit the Helm values file to configure your deployment:

```bash
cd ../helm/todo-chat
```

Update `values.yaml` with your Gemini API key:

```yaml
backend:
  env:
    GEMINI_API_KEY: "YOUR_ACTUAL_GEMINI_API_KEY_HERE"
```

**Important Configuration Notes:**

- **Database URL**: Pre-configured to use the local PostgreSQL pod
- **JWT Secret**: Change `JWT_SECRET` for production deployments
- **Database Password**: Change `postgresql.auth.password` for production
- **Image Pull Policy**: Set to `Never` for local images (already configured)

## Step 4: Deploy with Helm

Deploy the application to minikube:

```bash
# Create namespace (optional but recommended)
kubectl create namespace todo-chat

# Deploy using Helm from the helm directory
cd /Users/ammadkhan/coding/giaic-hackathon-2/phase3/helm
helm install todo-chat ./todo-chat --namespace todo-chat

# Or deploy from parent directory
# helm install todo-chat ./helm/todo-chat --namespace todo-chat

# Watch the pods starting up
kubectl get pods -n todo-chat -w
```

Wait for all pods to be in `Running` state and ready (1/1 or 2/2).

## Step 5: Access the Application

### Frontend (Recommended Method for Minikube)

```bash
# Get the URL for the frontend service
minikube service frontend --namespace todo-chat --url

# Or open directly in browser
minikube service frontend --namespace todo-chat
```

The frontend will be accessible at something like: `http://192.168.49.2:30080`

### Alternative Access Methods

#### Port Forwarding (if NodePort doesn't work)

```bash
# Forward frontend port
kubectl port-forward -n todo-chat svc/frontend 3000:3000

# Access at http://localhost:3000
```

#### Backend API (for testing)

```bash
# Forward backend port
kubectl port-forward -n todo-chat svc/backend 8000:8000

# Access API docs at http://localhost:8000/docs
```

## Step 6: Verify Deployment

### Check All Resources

```bash
# Check all pods
kubectl get pods -n todo-chat

# Check all services
kubectl get svc -n todo-chat

# Check persistent volumes
kubectl get pvc -n todo-chat

# Check secrets and configmaps
kubectl get secrets,configmaps -n todo-chat
```

### Check Logs

```bash
# Backend logs
kubectl logs -n todo-chat -l app.kubernetes.io/component=backend -f

# Frontend logs
kubectl logs -n todo-chat -l app.kubernetes.io/component=frontend -f

# Database logs
kubectl logs -n todo-chat -l app.kubernetes.io/component=database -f
```

### Test the Application

1. Open the frontend URL in your browser
2. Sign up for a new account
3. Log in with your credentials
4. Try creating a todo task via the chat interface:
   - "Add a task to buy groceries"
   - "What are my tasks?"
   - "Complete the task to buy groceries"

## Troubleshooting

### Pods Not Starting

```bash
# Describe pod to see events
kubectl describe pod -n todo-chat <pod-name>

# Check if images are available
minikube image ls | grep todo-chat
```

### Image Pull Errors

If you see `ImagePullBackOff` errors:

```bash
# Make sure you're using minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild images
cd backend && docker build -t todo-chat-backend:latest .
cd ../frontend && docker build -t todo-chat-frontend:latest .

# Verify imagePullPolicy is set to "Never" in values.yaml
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
kubectl get pods -n todo-chat | grep postgresql

# Check database logs
kubectl logs -n todo-chat -l app.kubernetes.io/component=database

# Verify database service
kubectl get svc -n todo-chat postgresql
```

### Backend API Errors

```bash
# Check backend logs for errors
kubectl logs -n todo-chat -l app.kubernetes.io/component=backend --tail=100

# Verify environment variables
kubectl exec -n todo-chat deployment/$(kubectl get deployment -n todo-chat -l app.kubernetes.io/component=backend -o name | cut -d'/' -f2) -- env | grep -E "DATABASE_URL|JWT_SECRET|GEMINI_API_KEY"
```

### Cannot Access Frontend

```bash
# Get minikube IP
minikube ip

# Get NodePort
kubectl get svc -n todo-chat frontend -o jsonpath='{.spec.ports[0].nodePort}'

# Access at http://<minikube-ip>:<nodeport>
```

## Updating the Deployment

### Update Configuration

```bash
# Edit values.yaml with your changes
nano helm/todo-chat/values.yaml

# Upgrade the deployment
helm upgrade todo-chat ./helm/todo-chat --namespace todo-chat
```

### Rebuild and Redeploy Images

```bash
# Point to minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild images
cd backend && docker build -t todo-chat-backend:latest .
cd ../frontend && docker build -t todo-chat-frontend:latest .

# Restart deployments to use new images
kubectl rollout restart deployment -n todo-chat
```

## Cleanup

### Uninstall the Application

```bash
# Uninstall Helm release
helm uninstall todo-chat --namespace todo-chat

# Delete namespace (optional)
kubectl delete namespace todo-chat

# Or delete PVCs manually if needed
kubectl delete pvc -n todo-chat --all
```

### Stop Minikube

```bash
# Stop minikube
minikube stop

# Delete minikube cluster (removes all data)
minikube delete
```

## Advanced Configuration

### Using Custom Values File

Create a custom values file for your environment:

```bash
# Create custom values
cat > values-local.yaml <<EOF
backend:
  env:
    GEMINI_API_KEY: "your-key-here"
    JWT_SECRET: "your-secret-here"

postgresql:
  auth:
    password: "secure-password"
EOF

# Deploy with custom values
helm install todo-chat ./helm/todo-chat -f values-local.yaml --namespace todo-chat
```

### Enabling Ingress

If you want to use a custom domain locally:

```bash
# Update values.yaml
ingress:
  enabled: true
  hosts:
    - host: todo-chat.local

# Update /etc/hosts
echo "$(minikube ip) todo-chat.local" | sudo tee -a /etc/hosts

# Deploy/upgrade
helm upgrade --install todo-chat ./helm/todo-chat --namespace todo-chat
```

## Performance Tuning

### Adjust Resource Limits

Edit `values.yaml` to adjust CPU and memory limits:

```yaml
backend:
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi
```

### Scale Deployments

```bash
# Scale backend
kubectl scale deployment -n todo-chat --replicas=2 \
  $(kubectl get deployment -n todo-chat -l app.kubernetes.io/component=backend -o name)

# Scale frontend
kubectl scale deployment -n todo-chat --replicas=2 \
  $(kubectl get deployment -n todo-chat -l app.kubernetes.io/component=frontend -o name)
```

## Monitoring

### View Resource Usage

```bash
# Pod resource usage
kubectl top pods -n todo-chat

# Node resource usage
kubectl top nodes
```

### Access Kubernetes Dashboard

```bash
# Start dashboard
minikube dashboard
```

## Next Steps

- Configure HTTPS/TLS for production
- Set up continuous deployment with CI/CD
- Add monitoring with Prometheus and Grafana
- Implement backup strategy for PostgreSQL data
- Configure horizontal pod autoscaling

## Support

For issues and questions:
- Check the logs: `kubectl logs -n todo-chat <pod-name>`
- Review the [Troubleshooting](#troubleshooting) section
- Verify all prerequisites are properly installed

---

**Happy deploying! 🚀**
