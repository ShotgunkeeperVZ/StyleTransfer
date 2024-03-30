#!/bin/bash

# Replace with the actual Google Drive folder ID from the share link
FOLDER_ID="1-91YINKzck0sOkFL8stqv4rAs7DEecE0"

# URL to download the folder
URL="https://drive.google.com/uc?export=download&id=$FOLDER_ID"

# Download the folder
wget --no-check-certificate "$URL" -O folder.zip

# Unzip the downloaded folder
unzip folder.zip

# Clean up: remove the zip file
rm folder.zip

echo "Folder downloaded and extracted successfully!"

conda env create -f environment.yml
conda install pip