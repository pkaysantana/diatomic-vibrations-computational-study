#!/bin/bash
# 1. Run Quantum Jobs
echo "Phase 1: Starting ORCA runs on AMD Ryzen..."
cd 1_quantum_mechanics/inputs
for mol in HCl DCl CO NO; do
    orca $mol.inp > ../outputs/$mol.out
done
cd ../..

# 2. Run Dynamics
echo "Phase 3: Unleashing 5070 Ti for GROMACS..."
cd 3_molecular_dynamics
gmx grompp -f parameters/nvt.mdp -c topology/HCl.gro -p topology/HCl.top -o analysis/nvt.tpr
gmx mdrun -v -deffnm analysis/nvt -nb gpu -pme gpu -bonded gpu -update gpu
cd ..

echo "All calcs finished. Ready for Python analysis."
