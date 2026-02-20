#!/bin/bash

# Todo Chat - Cleanup Script
# This script removes the Todo Chat deployment from minikube

set -e

echo "🧹 Cleaning up Todo Chat deployment"
echo "===================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if deployment exists
if helm list -n todo-chat | grep -q "todo-chat"; then
    echo "🗑️  Uninstalling Helm release..."
    helm uninstall todo-chat --namespace todo-chat
    echo -e "${GREEN}✓ Helm release uninstalled${NC}"
else
    echo -e "${YELLOW}⚠ No Helm release found${NC}"
fi

# Ask if user wants to delete namespace
echo ""
read -p "Do you want to delete the 'todo-chat' namespace? (This will remove all data) [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    kubectl delete namespace todo-chat
    echo -e "${GREEN}✓ Namespace deleted${NC}"
else
    echo "Keeping namespace 'todo-chat'"
fi

# Ask if user wants to remove images
echo ""
read -p "Do you want to remove Docker images from minikube? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    eval $(minikube docker-env)
    docker rmi todo-chat-backend:latest todo-chat-frontend:latest 2>/dev/null || true
    echo -e "${GREEN}✓ Images removed${NC}"
else
    echo "Keeping Docker images"
fi

echo ""
echo -e "${GREEN}✓ Cleanup complete!${NC}"
