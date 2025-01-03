#!/bin/bash

CONTAINERS=("mongodb" "tf_dev")

for CONTAINER in "${CONTAINERS[@]}"; do
    if docker ps --filter "name=$CONTAINER" --format '{{.Names}}' | grep -q "$CONTAINER"; then
        echo "Stopping and removing container: $CONTAINER..."
        docker stop "$CONTAINER"
    else
        echo "Container $CONTAINER is not running."
    fi
done