#!/bin/bash

# 🚀 AI Assistant Production Deployment Script
# This script deploys the AI Assistant to production server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
IMAGE_TAG="latest"
CONTAINER_NAME="ai-assistant-prod"
PORT="8000"
HEALTH_TIMEOUT="60"

# Function to print colored output
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   warning "Running as root. Consider using a non-root user for better security."
fi

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --image)
            IMAGE_TAG="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --container-name)
            CONTAINER_NAME="$2"
            shift 2
            ;;
        --help)
            echo "🚀 AI Assistant Production Deployment Script"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --image IMAGE_TAG        Docker image tag (default: latest)"
            echo "  --port PORT             Port to expose (default: 8000)"
            echo "  --container-name NAME   Container name (default: ai-assistant-prod)"
            echo "  --help                  Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0"
            echo "  $0 --image ghcr.io/user/ai-assistant:v1.0.0"
            echo "  $0 --port 3000 --container-name my-ai-assistant"
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

log "🚀 Starting AI Assistant deployment to production..."
log "📦 Image: $IMAGE_TAG"
log "🎯 Container: $CONTAINER_NAME"
log "🔌 Port: $PORT"

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker info &> /dev/null; then
    error "Docker daemon is not running. Please start Docker."
    exit 1
fi

# Pull the latest image
log "🔄 Pulling Docker image: $IMAGE_TAG"
if ! docker pull "$IMAGE_TAG"; then
    error "Failed to pull Docker image: $IMAGE_TAG"
    exit 1
fi
success "Image pulled successfully"

# Stop existing container if running
log "🛑 Stopping existing container if running..."
if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
    docker stop "$CONTAINER_NAME" || true
    success "Stopped existing container"
else
    log "No existing container found"
fi

# Remove existing container
log "🗑️ Removing existing container..."
if docker ps -a -q -f name="$CONTAINER_NAME" | grep -q .; then
    docker rm "$CONTAINER_NAME" || true
    success "Removed existing container"
fi

# Start new container
log "🚀 Starting new container..."
docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  -p "$PORT:8000" \
  -e ENVIRONMENT=production \
  -e API_HOST=0.0.0.0 \
  -e API_PORT=8000 \
  -e LOG_LEVEL=info \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  --health-start-period=40s \
  "$IMAGE_TAG"

if [ $? -eq 0 ]; then
    success "Container started successfully"
else
    error "Failed to start container"
    exit 1
fi

# Wait for container to be healthy
log "⏳ Waiting for container to be healthy (timeout: ${HEALTH_TIMEOUT}s)..."
counter=0
while [ $counter -lt $HEALTH_TIMEOUT ]; do
    if docker exec "$CONTAINER_NAME" curl -f -s http://localhost:8000/health > /dev/null 2>&1; then
        success "Container is healthy and responding!"
        break
    fi
    
    sleep 2
    counter=$((counter + 2))
    
    if [ $((counter % 10)) -eq 0 ]; then
        log "Still waiting... (${counter}s elapsed)"
    fi
done

if [ $counter -ge $HEALTH_TIMEOUT ]; then
    error "Container failed to become healthy within ${HEALTH_TIMEOUT} seconds"
    log "Container logs:"
    docker logs --tail 20 "$CONTAINER_NAME"
    exit 1
fi

# Final health check with detailed response
log "🔍 Running final health check..."
HEALTH_RESPONSE=$(docker exec "$CONTAINER_NAME" curl -s http://localhost:8000/health)
log "Health response: $HEALTH_RESPONSE"

# Get container details
CONTAINER_IP=$(docker inspect "$CONTAINER_NAME" --format '{{ .NetworkSettings.IPAddress }}' 2>/dev/null || echo "N/A")
CONTAINER_STATUS=$(docker inspect "$CONTAINER_NAME" --format '{{ .State.Status }}')

# Display deployment summary
echo ""
echo "🎉 =================================="
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "🎉 =================================="
echo ""
success "AI Assistant is now running in production!"
echo ""
echo "📊 Deployment Summary:"
echo "  🐳 Container Name: $CONTAINER_NAME"
echo "  📦 Image: $IMAGE_TAG"
echo "  🔌 Port: $PORT"
echo "  📍 Status: $CONTAINER_STATUS"
echo "  🌐 Container IP: $CONTAINER_IP"
echo ""
echo "🔗 Access URLs:"
echo "  🌍 API: http://localhost:$PORT"
echo "  📚 Documentation: http://localhost:$PORT/docs"
echo "  ❤️ Health Check: http://localhost:$PORT/health"
echo ""
echo "🤖 Your DevOps AI Assistant is ready!"
echo "   Try asking: 'what is kubernetes?' or 'explain docker containers'"
echo ""
echo "🔧 Container Management:"
echo "  📋 View logs: docker logs -f $CONTAINER_NAME"
echo "  🛑 Stop: docker stop $CONTAINER_NAME"
echo "  ♻️ Restart: docker restart $CONTAINER_NAME"
echo ""

# Optional: Show container logs
log "📋 Recent container logs:"
docker logs --tail 10 "$CONTAINER_NAME"

success "Deployment completed successfully! 🚀"