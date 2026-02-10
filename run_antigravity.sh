#!/bin/bash
# Antigravity Automation Master Script

# 1. Run Quantum Jobs
echo "Phase 1: Starting ORCA runs on AMD Ryzen (12 cores)..."
cd 1_quantum_mechanics/inputs
for mol in HCl DCl CO NO; do
    echo "Running ORCA for $mol..."
    # Check if orca is in path, otherwise warn
    if command -v orca &> /dev/null; then
        orca $mol.inp > ../outputs/$mol.out
    else
        echo "Warning: 'orca' command not found. Skipping $mol calculation."
    fi
done
cd ../..

# 2. Run Dynamics & Analysis
echo "Phase 3: Unleashing 5070 Ti for GROMACS..."
cd 3_molecular_dynamics

# 2a. Run Simulation
echo "  Running GROMACS MD..."
gmx grompp -f parameters/nvt.mdp -c topology/HCl.gro -p topology/HCl.top -o analysis/nvt.tpr
gmx mdrun -v -deffnm analysis/nvt -nb gpu -pme gpu -bonded gpu -update gpu

# 2b. Post-Processing (Generate dist.xvg)
echo "  Generating bond distance data..."
# Use '1 2' as input selection for bond distance (assuming index 1 and 2 are the atoms)
echo "1 2" | gmx distance -s analysis/nvt.tpr -f analysis/nvt.trr -o analysis/dist.xvg

# 2c. Run Python Analysis
echo "  Running FFT Analysis..."
cd analysis
python3 fft_analysis.py
cd ..

cd ..

# 3. Final Python Modeling
echo "Phase 2: Running Potential Energy Surface Analysis..."
cd 2_analysis_modeling
python3 reduced_mass.py
# Only run morse fit if output exists
if [ -f "../1_quantum_mechanics/outputs/HCl_PES_Scan.out" ]; then
    python3 morse_fit.py ../1_quantum_mechanics/outputs/HCl_PES_Scan.out
else
    echo "Skipping Morse fit (HCl_PES_Scan.out not found)."
fi
cd ..

echo "----------------------------------------------------------------"
echo "Antigravity Run Complete."
echo "Results:"
echo "  - ORCA Logs: 1_quantum_mechanics/outputs/"
echo "  - MD Plots:  3_molecular_dynamics/analysis/fft_spectrum.png"
echo "  - PES Plots: 2_analysis_modeling/plots/"
echo "----------------------------------------------------------------"
