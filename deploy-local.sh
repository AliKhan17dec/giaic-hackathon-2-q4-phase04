#!/bin/bash

# Todo Chat - Local Deployment Script
# This script automates the deployment of Todo Chat to minikube

set -e

echo "🚀 Todo Chat - Local Deployment Script"
echo "======================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if minikube is running
echo "📋 Checking prerequisites..."
if ! minikube status &> /dev/null; then
    echo -e "${RED}❌ Minikube is not running${NC}"
    echo "Starting minikube..."
    minikube start --driver=docker --memory=4096 --cpus=2
else
    echo -e "${GREEN}✓ Minikube is running${NC}"
fi

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo -e "${RED}❌ Helm is not installed${NC}"
    echo "Please install Helm: https://helm.sh/docs/intro/install/"
    exit 1
else
    echo -e "${GREEN}✓ Helm is installed${NC}"
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl is not installed${NC}"
    echo "Please install kubectl: https://kubernetes.io/docs/tasks/tools/"
    exit 1
else
    echo -e "${GREEN}✓ kubectl is installed${NC}"
fi

echo ""
echo "🐳 Building Docker images..."

# Point to minikube's Docker daemon
eval $(minikube docker-env)

# Build backend image
echo "Building backend image..."
cd backend
docker build -t todo-chat-backend:latest .
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend image built successfully${NC}"
else
    echo -e "${RED}❌ Failed to build backend image${NC}"
    exit 1
fi

# Build frontend image
echo "Building frontend image..."
cd ../frontend
docker build -t todo-chat-frontend:latest .
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend image built successfully${NC}"
else
    echo -e "${RED}❌ Failed to build frontend image${NC}"
    exit 1
fi

cd ..

# Verify images
echo ""
echo "📦 Verifying images in minikube..."
if minikube image ls | grep -q "todo-chat-backend" && minikube image ls | grep -q "todo-chat-frontend"; then
    echo -e "${GREEN}✓ Images are available in minikube${NC}"
else
    echo -e "${YELLOW}⚠ Images might not be properly loaded${NC}"
    echo "This might still work if you used 'eval \$(minikube docker-env)'"
fi

# Create namespace
echo ""
echo "📦 Creating namespace..."
kubectl create namespace todo-chat --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Namespace 'todo-chat' ready${NC}"

# Check if values file exists
if [ ! -f "helm/todo-chat/values.yaml" ]; then
    echo -e "${RED}❌ values.yaml not found${NC}"
    echo "Please make sure you're in the project root directory"
    exit 1
fi

# Deploy with Helm
echo ""
echo "🎯 Deploying with Helm..."
helm upgrade --install todo-chat ./helm/todo-chat \
    --namespace todo-chat \
    --wait \
    --timeout 5m

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Deployment successful!${NC}"
else
    echo -e "${RED}❌ Deployment failed${NC}"
    exit 1
fi

# Wait for pods to be ready
echo ""
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-chat -n todo-chat --timeout=300s

# Show deployment status
echo ""
echo "📊 Deployment Status:"
echo "===================="
kubectl get pods -n todo-chat

echo ""
echo "🌐 Services:"
echo "==========="
kubectl get svc -n todo-chat

# Get frontend URL
echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo ""
echo "To access the frontend, run:"
echo -e "${GREEN}minikube service frontend --namespace todo-chat${NC}"
echo ""
echo "Or get the URL with:"
echo -e "${GREEN}minikube service frontend --namespace todo-chat --url${NC}"
echo ""
echo "To view logs:"
echo "  Backend:  kubectl logs -n todo-chat -l app.kubernetes.io/component=backend -f"
echo "  Frontend: kubectl logs -n todo-chat -l app.kubernetes.io/component=frontend -f"
echo "  Database: kubectl logs -n todo-chat -l app.kubernetes.io/component=database -f"
echo ""
echo "To uninstall:"
echo "  helm uninstall todo-chat --namespace todo-chat"
echo ""
echo "Happy coding! 🚀"
