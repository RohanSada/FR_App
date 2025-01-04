#!/bin/bash

echo "Uninstalling FR Application..."

NETWORK_NAME="fr_network"
MONGO_IMAGE="mongo"
TF_DEV_IMAGE="tf_dev"
DATABASE_DIR="Database"

echo "Stopping and removing Docker containers..."
docker ps -a --filter "ancestor=$MONGO_IMAGE" --format "{{.ID}}" | xargs -r docker stop
docker ps -a --filter "ancestor=$TF_DEV_IMAGE" --format "{{.ID}}" | xargs -r docker stop
docker ps -a --filter "ancestor=$MONGO_IMAGE" --format "{{.ID}}" | xargs -r docker rm
docker ps -a --filter "ancestor=$TF_DEV_IMAGE" --format "{{.ID}}" | xargs -r docker rm

echo "Removing Docker images..."
docker images --filter "reference=$MONGO_IMAGE" --format "{{.ID}}" | xargs -r docker rmi
docker images --filter "reference=$TF_DEV_IMAGE" --format "{{.ID}}" | xargs -r docker rmi

if docker network inspect "$NETWORK_NAME" &>/dev/null; then
    echo "Removing Docker network..."
    docker network rm "$NETWORK_NAME"
else
    echo "Docker network $NETWORK_NAME does not exist."
fi

if [ -d "$DATABASE_DIR" ]; then
    echo "Removing Database directory..."
    rm -rf "$DATABASE_DIR"
    echo "Database directory removed."
else
    echo "Database directory does not exist."
fi

echo "FR Application uninstallation completed."