#!/bin/bash
# Pull a base image that has Python 3.10
base_image=python:3.10

# Create a new container from the base image
container=$(buildah from $base_image)

# Install Poetry on the container
# buildah run $container curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
buildah run $container python3 -m pip install -U pip poetry

# Set the working directory for the container
buildah config --workingdir /app $container

# Copy your pyproject.toml file and other Python files to the container
buildah copy $container pyproject.toml .

# Use Poetry to create and activate a virtual environment on the container
buildah run $container poetry shell

# Use Poetry to install dependencies on the container
buildah run $container poetry install

# Use Poetry to build your package on the container
# buildah run $container poetry build

# Set the entrypoint for the container
buildah config --entrypoint '["python", "main.py"]' $container

# Commit the container to an image
buildah commit --format docker $container python-app:latest

# Clean up the container
buildah rm $container
