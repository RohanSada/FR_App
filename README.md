# Face Recognition (FR) Application

This repository contains an end-to-end Face Recognition (FR) application developed using Python 3, Docker, and Flask. It provides functionalities such as face detection, recognition, and embedding storage using a MongoDB backend.

---

## Features

- **Face Recognition Server**: Powered by Flask and TensorFlow.
- **Database Support**: MongoDB for storing face embeddings.
- **Dockerized Deployment**: Simplified setup with Docker containers.
- **Configurable**: Easily customize server, database, and model paths via a JSON configuration file.

---

## Prerequisites

Ensure you have the following:

- **Docker Desktop** installed on your system. Download it [here](https://www.docker.com/products/docker-desktop).

---

## Installation

Run the `install.sh` script to prepare the application:

```bash
bash install.sh
```

---

## Starting the Application

Run the `start.sh` script to start the application:

```bash
bash start.sh
```
- What this script does:
- Starts the MongoDB container on port 27017.
- Launches the Face Recognition server on port 3000.
- Once the application starts, you can access the server at:
- Localhost: http://127.0.0.1:3000

---

## Stop the Application

Run the `stop.sh` script to stop the application

```bash
bash stop.sh
```

---

## Uninstall the Application

Run the `uninstall.sh` script to uninstall the applicaiton

```bash
bash uninstall.sh
```
