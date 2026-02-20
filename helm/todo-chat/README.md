# Todo Chat Helm Chart

A Helm chart for deploying the Todo Chat application with AI agent integration on Kubernetes.

## Features

- **Backend**: FastAPI application with OpenAI Agents SDK
- **Frontend**: Next.js web application
- **Database**: PostgreSQL for persistent storage
- **Secrets Management**: Kubernetes Secrets for sensitive data
- **ConfigMaps**: Environment configuration management
- **Persistent Storage**: PersistentVolumeClaim for database
- **Health Checks**: Liveness and readiness probes
- **Resource Limits**: CPU and memory constraints

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- PV provisioner support in the underlying infrastructure (for PostgreSQL persistence)

## Installing the Chart

### Local Minikube Deployment

```bash
# Install with default values
helm install todo-chat ./todo-chat --namespace todo-chat --create-namespace

# Install with local values (includes configuration for minikube)
helm install todo-chat ./todo-chat -f values-local.yaml --namespace todo-chat --create-namespace
```

### Custom Installation

```bash
# Create custom values file
cat > my-values.yaml <<EOF
backend:
  env:
    GEMINI_API_KEY: "your-api-key-here"
postgresql:
  auth:
    password: "secure-password"
EOF

# Install with custom values
helm install todo-chat ./todo-chat -f my-values.yaml --namespace todo-chat --create-namespace
```

## Uninstalling the Chart

```bash
helm uninstall todo-chat --namespace todo-chat
```

## Configuration

The following table lists the configurable parameters of the Todo Chat chart and their default values.

### Global Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.environment` | Environment type (local/production) | `local` |

### Backend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.enabled` | Enable backend deployment | `true` |
| `backend.replicaCount` | Number of backend replicas | `1` |
| `backend.image.repository` | Backend image repository | `todo-chat-backend` |
| `backend.image.tag` | Backend image tag | `latest` |
| `backend.image.pullPolicy` | Image pull policy | `Never` |
| `backend.service.type` | Kubernetes service type | `ClusterIP` |
| `backend.service.port` | Service port | `8000` |
| `backend.env.DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@postgresql:5432/todochat` |
| `backend.env.JWT_SECRET` | JWT secret key | `a-very-secret-key-change-in-production` |
| `backend.env.GEMINI_API_KEY` | Gemini API key | `""` |
| `backend.resources.limits.cpu` | CPU limit | `500m` |
| `backend.resources.limits.memory` | Memory limit | `512Mi` |

### Frontend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.enabled` | Enable frontend deployment | `true` |
| `frontend.replicaCount` | Number of frontend replicas | `1` |
| `frontend.image.repository` | Frontend image repository | `todo-chat-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `frontend.image.pullPolicy` | Image pull policy | `Never` |
| `frontend.service.type` | Kubernetes service type | `NodePort` |
| `frontend.service.port` | Service port | `3000` |
| `frontend.service.nodePort` | NodePort (if type is NodePort) | `30080` |
| `frontend.env.NEXT_PUBLIC_API_URL` | Backend API URL | `http://backend:8000` |
| `frontend.resources.limits.cpu` | CPU limit | `300m` |
| `frontend.resources.limits.memory` | Memory limit | `256Mi` |

### PostgreSQL Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `postgresql.enabled` | Enable PostgreSQL deployment | `true` |
| `postgresql.image.repository` | PostgreSQL image repository | `postgres` |
| `postgresql.image.tag` | PostgreSQL image tag | `15-alpine` |
| `postgresql.service.port` | Service port | `5432` |
| `postgresql.auth.database` | Database name | `todochat` |
| `postgresql.auth.username` | Database username | `postgres` |
| `postgresql.auth.password` | Database password | `postgres` |
| `postgresql.persistence.enabled` | Enable persistent storage | `true` |
| `postgresql.persistence.size` | Storage size | `1Gi` |
| `postgresql.persistence.storageClass` | Storage class | `standard` |
| `postgresql.resources.limits.cpu` | CPU limit | `500m` |
| `postgresql.resources.limits.memory` | Memory limit | `512Mi` |

### Ingress Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | Ingress class name | `nginx` |
| `ingress.hosts` | Ingress hosts configuration | `[]` |

## Examples

### Scaling the Application

```bash
# Scale backend to 3 replicas
helm upgrade todo-chat ./todo-chat --set backend.replicaCount=3 --namespace todo-chat

# Scale frontend to 2 replicas
helm upgrade todo-chat ./todo-chat --set frontend.replicaCount=2 --namespace todo-chat
```

### Updating Configuration

```bash
# Update Gemini API key
helm upgrade todo-chat ./todo-chat \
  --set backend.env.GEMINI_API_KEY="new-api-key" \
  --namespace todo-chat

# Update database password
helm upgrade todo-chat ./todo-chat \
  --set postgresql.auth.password="new-secure-password" \
  --namespace todo-chat
```

### Enabling Ingress

```bash
helm upgrade todo-chat ./todo-chat \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=todo-chat.local \
  --namespace todo-chat
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n todo-chat

# Describe pod to see events
kubectl describe pod -n todo-chat <pod-name>

# Check logs
kubectl logs -n todo-chat <pod-name>
```

### Image Pull Errors

If using local images with minikube:
- Ensure `imagePullPolicy` is set to `Never`
- Build images in minikube's Docker daemon: `eval $(minikube docker-env)`
- Verify images are available: `minikube image ls | grep todo-chat`

### Database Connection Issues

```bash
# Check if PostgreSQL is running
kubectl get pods -n todo-chat | grep postgresql

# Check PostgreSQL logs
kubectl logs -n todo-chat -l app.kubernetes.io/component=database

# Verify service
kubectl get svc -n todo-chat postgresql
```

## Support

For issues and questions, please refer to the main project documentation.

## License

[Your License Here]
