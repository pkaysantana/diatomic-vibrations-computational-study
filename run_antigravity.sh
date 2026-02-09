#!/bin/bash
# Antigravity Automation Master Script

# 1. Run all QM jobs on the AMD Ryzen (12 cores)
echo "Starting Phase 1: Quantum Mechanical Optimizations..."
cd 1_quantum_mechanics/inputs
for mol in HCl DCl CO NO; do
    echo "Running $mol..."
    orca $mol.inp > ../outputs/$mol.out
done
cd ../..

# 2. Setup and run GROMACS on the RTX 5070 Ti
echo "Starting Phase 3: GPU-Accelerated Molecular Dynamics..."
cd 3_molecular_dynamics
gmx grompp -f parameters/nvt.mdp -c topology/HCl.gro -p topology/HCl.top -o analysis/nvt.tpr
gmx mdrun -v -deffnm analysis/nvt -nb gpu -pme gpu -bonded gpu -update gpu
cd ..

echo "Antigravity Run Complete. Check analysis/ for FFT data."
