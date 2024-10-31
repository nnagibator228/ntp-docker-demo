#!/bin/bash

command_exists() {
    command -v "$1" >/dev/null 2>&1
}
if ! command_exists docker; then
    echo "Error: Docker is not installed."
    exit 1
fi
if ! command_exists docker buildx; then
    echo "Error: Docker Buildx is not installed."
    exit 1
fi
if ! command_exists docker compose; then
    echo "Error: Docker Compose v2 is not installed."
    exit 1
fi
if [ ! -d "./chrony-docker" ]; then
    echo "Error: ./chrony-docker directory does not exist."
    exit 1
fi
if [ ! -f ".front.env" ]; then
    echo "Error: .front.env file does not exist."
    exit 1
fi
if [ ! -f ".main.env" ]; then
    echo "Error: .main.env file does not exist."
    exit 1
fi

echo "Building Docker image..."
docker build -t custom/chrony:local ./chrony-docker
echo "Running docker compose up -d..."
docker compose up -d
