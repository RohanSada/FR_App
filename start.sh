#!/bin/bash

echo "Starting MongoDB container..."
docker run --rm -d --name mongodb --network fr_network -p 27017:27017 -v ./database:/data/db mongo
echo "MongoDB started!"

echo "Starting FR Server"
docker run --rm -d -it --network fr_network -p 3000:3000 -w /usr/src/app --name tf_dev tf_dev python3 ./main.py ./config.json

echo "Running on all addresses (0.0.0.0)
Running on http://127.0.0.1:3000
Running on http://172.17.0.2:3000"
