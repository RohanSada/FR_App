#!/bin/bash

NETWORK_NAME="fr_network"

if ! docker network inspect "$NETWORK_NAME" &>/dev/null; then
    docker network create "$NETWORK_NAME"
fi

echo "Starting MongoDB container..."
docker run --rm -d --name mongodb --network "$NETWORK_NAME" -p 27017:27017 -v ./database:/data/db mongo
echo "MongoDB started!"

echo "Starting FR Server"
docker run --rm -d -it -v ./:/usr/src/app --network "$NETWORK_NAME" -p 3000:3000 -w /usr/src/app --name tf_dev tf_dev python3 ./main.py ./config.json

echo "Running on all addresses (0.0.0.0)
Running on http://127.0.0.1:3000
Running on http://172.17.0.2:3000"
