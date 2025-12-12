#!/bin/bash

# Define your Docker Hub username and image tag
DOCKERHUB_USERNAME="aryanvaghasiya" # <--- IMPORTANT: Change this to your Docker Hub username
BASE_IMAGE_TAG="py3.11-carecompass-base-torch-2.5.1" # Using a more descriptive tag

FULL_IMAGE_NAME="${DOCKERHUB_USERNAME}/carecompass-base:${BASE_IMAGE_TAG}"

echo "Building Docker base image: ${FULL_IMAGE_NAME}"

# Build the base image
docker build -t "${FULL_IMAGE_NAME}" -f Dockerfile.base .

if [ $? -eq 0 ]; then
    echo "Docker base image built successfully."
    echo "Logging into Docker Hub..."
    docker login -u "${DOCKERHUB_USERNAME}"

    if [ $? -eq 0 ]; then
        echo "Pushing Docker base image to Docker Hub..."
        docker push "${FULL_IMAGE_NAME}"

        if [ $? -eq 0 ]; then
            echo "Docker base image pushed successfully to Docker Hub."
        else
            echo "Error: Failed to push Docker base image."
            exit 1
        fi
    else
        echo "Error: Failed to log in to Docker Hub. Please check your username and password."
        exit 1
    fi
else
    echo "Error: Failed to build Docker base image."
    exit 1
fi
