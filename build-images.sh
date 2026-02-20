#!/bin/bash

# Todo Chat - Build Images Script
# This script builds Docker images and loads them into minikube

set -e

echo "🐳 Building Docker Images for Minikube"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo -e "${YELLOW}⚠ Minikube is not running. Starting minikube...${NC}"
    minikube start --driver=docker --memory=4096 --cpus=2
fi

# Point to minikube's Docker daemon
echo "🔗 Connecting to minikube's Docker daemon..."
eval $(minikube docker-env)

# Build backend image
echo ""
echo "📦 Building backend image..."
cd backend
docker build -t todo-chat-backend:latest .
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend image built successfully${NC}"
else
    echo "❌ Failed to build backend image"
    exit 1
fi

# Build frontend image
echo ""
echo "📦 Building frontend image..."
cd ../frontend
docker build -t todo-chat-frontend:latest .
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend image built successfully${NC}"
else
    echo "❌ Failed to build frontend image"
    exit 1
fi

cd ..

# List images
echo ""
echo "📋 Available images in minikube:"
docker images | grep -E "REPOSITORY|todo-chat"

echo ""
echo -e "${GREEN}✓ All images built successfully!${NC}"
echo ""
echo "Next steps:"
echo "  1. Update helm/todo-chat/values.yaml with your GEMINI_API_KEY"
echo "  2. Run: ./deploy-local.sh"
