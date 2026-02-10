#!/bin/bash
# install_orca.sh
# Automates ORCA and GROMACS installation

echo "--------------------------------------------------------"
echo "Starting Installation Script (v2 - Robust)"
echo "--------------------------------------------------------"

# 1. Environment Check
if [[ "$(uname -r)" != *microsoft* && "$(uname)" != "Linux" ]]; then
    echo "This script must run inside WSL. Launching WSL..."
    wsl bash install_orca.sh
    exit $?
fi

# 2. Install GROMACS (requires sudo, might ask for password)
echo "Checking for GROMACS..."
if ! command -v gmx &> /dev/null; then
    echo "GROMACS not found. Installing..."
    echo "Please enter your password if prompted."
    sudo apt-get update
    sudo apt-get install -y gromacs
else
    echo "GROMACS is already installed."
fi

# 3. Install ORCA
DOWNLOADS_DIR="/mnt/c/Users/Don/Downloads"
TARGET_DIR="$HOME/orca_6_1_0"
SYMLINK_DIR="$HOME/orca"

echo "Looking for ORCA in Downloads..."

# Find ANY folder starting with orca_6 in Downloads
FOUND_ORCA=$(find "$DOWNLOADS_DIR" -maxdepth 1 -type d -name "orca_6*" | head -n 1)

if [ -z "$FOUND_ORCA" ]; then
    echo "Error: Could not find any extracted ORCA folder in Downloads."
    echo "Please ensure you downloaded AND extracted ORCA to your Downloads folder."
    exit 1
fi

echo "Found ORCA source: $FOUND_ORCA"

if [ -d "$TARGET_DIR" ]; then
    echo "Target directory $TARGET_DIR already exists."
else
    echo "Moving ORCA to $TARGET_DIR..."
    mv "$FOUND_ORCA" "$TARGET_DIR"
fi

# Force Symlink creation
ln -sfn "$TARGET_DIR" "$SYMLINK_DIR"
echo "Updated symlink at $SYMLINK_DIR"

# 4. Configure PATH
echo "Configuring PATH in ~/.bashrc..."
if ! grep -q "export PATH=\"\$HOME/orca:\$PATH\"" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# ORCA via Antigravity Setup" >> ~/.bashrc
    echo "export PATH=\"\$HOME/orca:\$PATH\"" >> ~/.bashrc
    echo "export LD_LIBRARY_PATH=\"\$HOME/orca:\$LD_LIBRARY_PATH\"" >> ~/.bashrc
    echo "PATH updated."
fi

echo "--------------------------------------------------------"
echo "Installation Complete!"
echo "IMPORTANT: RUN THIS COMMAND NOW:"
echo "source ~/.bashrc"
echo "--------------------------------------------------------"
