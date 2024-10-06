#!/bin/bash

echo "Updating package list and upgrading existing packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

packages=(
    "poppler-utils"
    "libreoffice"
    "tesseract-ocr"
    "libtesseract-dev"
)

echo "Installing packages..."
for package in "${packages[@]}"; do
    echo "Installing $package..."
    sudo apt-get install -y $package
done

echo "All packages installed successfully!"
