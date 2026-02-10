#!/bin/bash
# install_orca.sh
# Automates moving ORCA from Windows Downloads to WSL Home and updating PATH

DOWNLOADS_DIR="/mnt/c/Users/Don/Downloads"
ORCA_FOLDER="orca_6_1_0_linux_x86-64_shared_openmpi418_avx2"
TARGET_DIR="$HOME/orca_6_1_0"
SYMLINK_DIR="$HOME/orca"

echo "Checking for ORCA in Downloads..."

if [ ! -d "$DOWNLOADS_DIR/$ORCA_FOLDER" ]; then
    echo "Error: Could not find ORCA folder in Downloads."
    echo "Looked for: $DOWNLOADS_DIR/$ORCA_FOLDER"
    echo "Please ensure you have extracted the downloaded file."
    exit 1
fi

echo "Found ORCA. Moving to $TARGET_DIR..."
# Use rsync for better progress or just mv
# Check if target exists
if [ -d "$TARGET_DIR" ]; then
    echo "Target directory $TARGET_DIR already exists. Skipping copy."
else
    mv "$DOWNLOADS_DIR/$ORCA_FOLDER" "$TARGET_DIR"
fi

# Create symlink for easier access
ln -sZnf "$TARGET_DIR" "$SYMLINK_DIR"

echo "Configuring PATH in ~/.bashrc..."

# Check if already added
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
