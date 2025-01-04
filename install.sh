#!/bin/bash

echo "Installing FR Application"

if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

if [ -d "Database" ]; then
    echo "Removing existing Database directory..."
    rm -rf Database
fi
echo "Creating Database directory..."
mkdir Database
echo "Database directory is ready."

NETWORK_NAME="fr_network"

if ! docker network inspect "$NETWORK_NAME" &>/dev/null; then
    docker network create "$NETWORK_NAME"
fi

echo "Building Docker Images..."
docker build -t tf_dev -f Dockerfile.server .
docker build -t mongo -f Dockerfile.mongo .

echo "FR Application setup completed."