#!/bin/bash

# Start script for Linux
# Builds and runs the Docker container for PM Kanban app

set -e

echo "Building Docker image..."
docker build -t pm-kanban:latest .

echo "Starting container..."
docker run -d \
  --name pm-kanban \
  -p 8000:8000 \
  --env-file .env \
  pm-kanban:latest

echo "Container started successfully!"
echo "API is available at http://localhost:8000"
echo "Health check: curl http://localhost:8000/health"
echo "To view logs: docker logs -f pm-kanban"
echo "To stop: ./scripts/stop-linux.sh"
