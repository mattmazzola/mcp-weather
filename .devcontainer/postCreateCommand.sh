#! /bin/bash

set -e

echo "INSTALLING PROJECT DEPENDENCIES"

# Install project dependencies with UV
uv sync

echo "postCreateCommand.sh finished!"
