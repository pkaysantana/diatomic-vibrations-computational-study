#!/bin/bash
# Antigravity Automation Master Script

# Environment Setup
echo "Phase -1: Setting up Python Environment in WSL..."

# Use a location in the Linux home directory to avoid /mnt/c verify permission issues
VENV_DIR="$HOME/.antigravity_venv"

if [ -d "$VENV_DIR" ] && [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "Detected broken venv at $VENV_DIR. Removing..."
    rm -rf "$VENV_DIR"
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Warning: Standard venv creation failed. Trying fallback without pip..."
        rm -rf "$VENV_DIR"
        python3 -m venv "$VENV_DIR" --without-pip
        if [ $? -ne 0 ]; then
            echo "Error: Failed to create venv even without pip. Please install python3-venv."
            exit 1
        fi
        
        source "$VENV_DIR/bin/activate"
        echo "Bootstrapping pip..."
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    fi
fi


# 2. Activate Virtual Environment (Cross-Platform)
if [ -f "$VENV_DIR/Scripts/activate" ]; then
    # Windows / Git Bash
    source "$VENV_DIR/Scripts/activate"
    PYTHON_BIN="$VENV_DIR/Scripts/python"
    PIP_BIN="$VENV_DIR/Scripts/pip"
elif [ -f "$VENV_DIR/bin/activate" ]; then
    # Linux / WSL
    source "$VENV_DIR/bin/activate"
    PYTHON_BIN="$VENV_DIR/bin/python3"
    PIP_BIN="$VENV_DIR/bin/pip"
else
    echo "Error: Virtual Environment created at $VENV_DIR but activate script not found."
    echo "Check if creation failed or if path is correct."
    exit 1
fi

echo "Installing dependencies..."
"$PIP_BIN" install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies. Please ensure python3-venv and python3-pip are installed."
    exit 1
fi




# Explicitly add ORCA to PATH for this script execution
# Found structure: ~/orca -> orca_6_1_0... folder
# So binary is at ~/orca/orca_6_1_0_linux_x86-64_shared_openmpi418_avx2/orca
ORCA_HOME="$HOME/orca/orca_6_1_0_linux_x86-64_shared_openmpi418_avx2"
export PATH="$ORCA_HOME:$PATH"
export LD_LIBRARY_PATH="$ORCA_HOME:$LD_LIBRARY_PATH"

# Check if ORCA is actually found
if ! command -v orca &> /dev/null; then
    echo "WARNING: 'orca' command still not found in PATH."
    echo "Attempting to locate it dynamically..."
    DYNAMIC_ORCA=$(find "$HOME/orca" -name "orca" -type f -executable | head -n 1)
    if [ -n "$DYNAMIC_ORCA" ]; then
        ORCA_DIR=$(dirname "$DYNAMIC_ORCA")
        export PATH="$ORCA_DIR:$PATH"
        export LD_LIBRARY_PATH="$ORCA_DIR:$LD_LIBRARY_PATH"
        # Also set ORCA_PATH for good measure
        export ORCA_PATH="$ORCA_DIR" 
        echo "Found ORCA at: $ORCA_DIR"
    fi
fi

# Ensure MD inputs exist
echo "Generating missing MD input files..."
"$PYTHON_BIN" generate_md_inputs.py

# 0. Mock Data Check (DISABLED BY USER)




# 0. Self-Test Phase
echo "Phase 0: Running Unit Tests..."
"$PYTHON_BIN" -m unittest discover tests
if [ $? -ne 0 ]; then
    echo "CRITICAL ERROR: Unit tests failed. Aborting production run."
    exit 1
fi
echo "Unit tests passed. Proceeding..."

# 1. Run Quantum Jobs
echo "Phase 1: Starting ORCA runs on AMD Ryzen (12 cores)..."
cd 1_quantum_mechanics/inputs
for mol in HCl DCl CO NO; do
    echo "Running ORCA for $mol..."
    # Check if orca is available and get full path
    ORCA_FULL_PATH=$(command -v orca)
    if [ -n "$ORCA_FULL_PATH" ]; then
        "$ORCA_FULL_PATH" $mol.inp > ../outputs/$mol.out
    else
        echo "Warning: 'orca' command not found. Skipping $mol calculation."
    fi
done
cd ../..

# 2. Run Dynamics & Analysis
echo "Phase 3: Unleashing 5070 Ti for GROMACS..."
cd 3_molecular_dynamics

# Check if GROMACS is installed
if command -v gmx &> /dev/null; then
    # 2a. Run Simulation
    echo "  Running GROMACS MD..."
    gmx grompp -f parameters/nvt.mdp -c topology/HCl.gro -p topology/HCl.top -o analysis/nvt.tpr
    gmx mdrun -v -deffnm analysis/nvt

    # 2b. Post-Processing (Generate dist.xvg)
    echo "  Generating bond distance data..."
    # Use '1 2' as input selection for bond distance (assuming index 1 and 2 are the atoms)
    gmx distance -s analysis/nvt.tpr -f analysis/nvt.trr -oall analysis/dist.xvg -select 'com of group 1, com of group 2'
elif [ -f "analysis/dist.xvg" ]; then
    echo "  Warning: 'gmx' command not found, but 'dist.xvg' exists."
    echo "  Using existing data for analysis."
else
    echo "  Error: 'gmx' command not found and no existing 'dist.xvg' found."
    echo "  Cannot proceed with FFT analysis."
fi

# 2c. Run Python Analysis
echo "  Running FFT Analysis..."
cd analysis
"$PYTHON_BIN" fft_analysis.py
cd ..

cd ..

# 3. Final Python Modeling
echo "Phase 2: Running Potential Energy Surface Analysis..."
cd 2_analysis_modeling
"$PYTHON_BIN" reduced_mass.py
# Only run morse fit if output exists
if [ -f "../1_quantum_mechanics/outputs/HCl_PES_Scan.out" ]; then
    "$PYTHON_BIN" morse_fit.py ../1_quantum_mechanics/outputs/HCl_PES_Scan.out
else
    echo "Skipping Morse fit (HCl_PES_Scan.out not found)."
fi
cd ..

# 4. Final Validation
echo "Phase 4: Quantitative Validation against NIST Data..."
"$PYTHON_BIN" validation/benchmark_compare.py


echo "----------------------------------------------------------------"
echo "Antigravity Run Complete."
echo "Results:"
echo "  - ORCA Logs: 1_quantum_mechanics/outputs/"
echo "  - MD Plots:  3_molecular_dynamics/analysis/fft_spectrum.png"
echo "  - PES Plots: 2_analysis_modeling/plots/"
echo "----------------------------------------------------------------"
