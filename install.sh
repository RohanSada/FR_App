#!/bin/bash

echo "Installing FR Application"

if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

echo "Extracting and loading docker images..."
zstd -dc ./docker_images/tf_dev.tar.zst | docker load
zstd -dc ./docker_images/mongo.tar.zst | docker load
echo "Images Loaded"

if [ -d "Database" ]; then
    echo "Removing existing Database directory..."
    rm -rf Database
fi
echo "Creating Database directory..."
mkdir Database
echo "Database directory is ready."

echo "FR Application setup completed."