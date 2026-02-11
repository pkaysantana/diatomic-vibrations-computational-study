#!/bin/bash
# Antigravity High-Performance Research Pipeline
# Optimized for: AMD Ryzen 9 9955HX (16 Cores) | 64GB RAM | RTX 5070 Ti

# 1. Environment Setup
VENV_DIR="$HOME/.antigravity_venv"
source "$VENV_DIR/bin/activate"
PYTHON_BIN="$VENV_DIR/bin/python3"

# ORCA Discovery & Explicit Indexing (CRITICAL FOR PARALLEL RUNS)
ORCA_DIR="$HOME/orca/orca_6_1_0_linux_x86-64_shared_openmpi418_avx2"
if [ ! -d "$ORCA_DIR" ]; then
    ORCA_DIR=$(find "$HOME/orca" -name "orca" -type f -executable | head -n 1 | xargs dirname)
fi
ORCA_BIN="$ORCA_DIR/orca"
export PATH="$ORCA_DIR:$PATH"
export LD_LIBRARY_PATH="$ORCA_DIR:$LD_LIBRARY_PATH"

echo "----------------------------------------------------------------"
echo "PHASE 0: Hardware Optimization & Dependency Verification"
echo "----------------------------------------------------------------"
"$PYTHON_BIN" generate_md_inputs.py
"$PYTHON_BIN" -m unittest discover tests

echo "----------------------------------------------------------------"
echo "PHASE 1: Quantum Chemistry (ORCA 6.1.0)"
echo "Theory: Optimized PBE0/def2-TZVP (Ref) & CCSD(T) (Scan)"
echo "Compute: 12 R9 Cores | 48GB RAM"
echo "----------------------------------------------------------------"
cd 1_quantum_mechanics/inputs

# Update standard runs to 12 cores with absolute binary call
for mol in HCl DCl CO NO; do
    echo "  Executing $mol optimization (12 Cores)..."
    # Ensure %pal nprocs 12 and %maxcore 4000 are set accurately
    sed -i 's/nprocs [0-9]*/nprocs 12/g' $mol.inp
    if grep -q "%maxcore" $mol.inp; then
        sed -i 's/%maxcore [0-9]*/%maxcore 4000/g' $mol.inp
    else
        sed -i '1i %maxcore 4000' $mol.inp
    fi
    "$ORCA_BIN" $mol.inp > ../outputs/$mol.out
done

# High-Accuracy PES Scan (Manual Python Loop for Robustness)
echo "  Executing Gold-Standard PES Scan: DLPNO-CCSD(T)/cc-pVQZ..."
# Export absolute path for Python script
export ORCA_FULL_PATH="$ORCA_BIN"
"$PYTHON_BIN" run_pes_scan.py

cd ../..

echo "----------------------------------------------------------------"
echo "PHASE 2: GROMACS Molecular Dynamics"
echo "----------------------------------------------------------------"
cd 3_molecular_dynamics
gmx grompp -f parameters/nvt.mdp -c topology/HCl.gro -p topology/HCl.top -o analysis/nvt.tpr
# GPU Fallback Logic: Try GPU first, then CPU
gmx mdrun -v -deffnm analysis/nvt -nb gpu -pme gpu -bonded gpu -pin on 2>/dev/null || \
gmx mdrun -v -deffnm analysis/nvt -pin on

# Bond Distance Extraction
gmx distance -s analysis/nvt.tpr -f analysis/nvt.trr -oall analysis/dist.xvg -select 'atomnr 1 or atomnr 2'
cd analysis
"$PYTHON_BIN" fft_analysis.py
cd ../..

echo "----------------------------------------------------------------"
echo "PHASE 3: Final Analysis & Validation"
echo "----------------------------------------------------------------"
cd 2_analysis_modeling
"$PYTHON_BIN" reduced_mass.py
"$PYTHON_BIN" morse_fit.py ../1_quantum_mechanics/outputs/HCl_PES_Scan.out
cd ..
"$PYTHON_BIN" validation/benchmark_compare.py

echo "----------------------------------------------------------------"
echo "Project COMPLETE | Results exported to analysis/ and validation/"
echo "----------------------------------------------------------------"
