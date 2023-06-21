#!/bin/bash

# Define variables
IMAGE_NAME="wordnet-microservice"
CONTAINER_NAME="wordnet"

# Check if the container is running, stop and remove it
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    echo "Container $CONTAINER_NAME is running. Stopping and removing..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
    echo "Container $CONTAINER_NAME has been stopped and removed."
fi

# Build a new Docker image
echo "Building new Docker image with name $IMAGE_NAME..."
docker build -t $IMAGE_NAME .

# Run a new container from the new image
echo "Running a new Docker container with name $CONTAINER_NAME..."
docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME

echo "Script completed."
