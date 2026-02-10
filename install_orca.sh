#!/bin/bash
# install_orca.sh
# Automates moving ORCA from Windows Downloads to WSL Home and updating PATH
# Created by Antigravity

echo "Starting ORCA Installation Script..."

# Detect Environment (WSL vs Git Bash)
if [[ "$(uname -r)" != *microsoft* && "$(uname)" != "Linux" ]]; then
    echo "Detected Windows environment (Git Bash/PowerShell)."
    echo "This script must run inside WSL. Attempting to relaunch..."
    wsl bash install_orca.sh
    if [ $? -eq 0 ]; then exit 0; else echo "Error: Failed to launch script inside WSL."; exit 1; fi
fi

# Define Paths
DOWNLOADS_DIR="/mnt/c/Users/Don/Downloads"
ORCA_FOLDER_NAME="orca_6_1_0_linux_x86-64_shared_openmpi418_avx2"
SOURCE_PATH="$DOWNLOADS_DIR/$ORCA_FOLDER_NAME"
TARGET_DIR="$HOME/orca_6_1_0"
SYMLINK_DIR="$HOME/orca"

echo "Looking for ORCA in: $DOWNLOADS_DIR"

if [ ! -d "$SOURCE_PATH" ]; then
    echo "Error: Could not find extracted ORCA folder at:"
    echo "  $SOURCE_PATH"
    echo ""
    echo "Checking for alternative versions..."
    ls -d "$DOWNLOADS_DIR"/orca_* 2>/dev/null
    exit 1
fi

echo "Found ORCA folder. Installing to: $TARGET_DIR"

# Move/Copy
if [ -d "$TARGET_DIR" ]; then
    echo "Target directory $TARGET_DIR already exists."
    echo "Skipping copy (assuming it's installed)."
else
    mv "$SOURCE_PATH" "$TARGET_DIR"
    echo "Moved folder successfully."
fi

# Create Symlink
ln -sZnf "$TARGET_DIR" "$SYMLINK_DIR"
echo "Created symlink at $SYMLINK_DIR"

# Update PATH
echo "Configuring PATH in ~/.bashrc..."
if grep -q "export PATH=\"\$HOME/orca:\$PATH\"" ~/.bashrc; then
    echo "PATH already configured in .bashrc."
else
    echo "" >> ~/.bashrc
    echo "# ORCA via Antigravity Setup" >> ~/.bashrc
    echo "export PATH=\"\$HOME/orca:\$PATH\"" >> ~/.bashrc
    echo "export LD_LIBRARY_PATH=\"\$HOME/orca:\$LD_LIBRARY_PATH\"" >> ~/.bashrc
    echo "PATH updated."
fi

echo "--------------------------------------------------------"
echo "Installation Complete!"
echo "IMPORTANT: Run the following command to apply changes:"
echo "source ~/.bashrc"
echo "--------------------------------------------------------"
