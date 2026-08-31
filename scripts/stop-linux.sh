#!/bin/bash

# Stop script for Linux
# Stops and removes the Docker container

set -e

echo "Stopping container..."
docker stop pm-kanban || true

echo "Removing container..."
docker rm pm-kanban || true

echo "Container stopped and removed successfully!"
