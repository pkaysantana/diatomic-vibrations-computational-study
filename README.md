# Diatomic Vibrations Computational Study

## Abstract
A multi-scale computational study of diatomic vibrations (HCl, DCl, CO, NO). This project integrates B3LYP/def2-TZVP quantum calculations via ORCA, Morse potential surface mapping in Python, and GROMACS MD simulations. Optimized for AMD/NVIDIA hardware to validate isotope effects, bond anharmonicity, and FFT-derived spectroscopic observables.

## Project Structure

### 1. Quantum Mechanics (`1_quantum_mechanics/`)
Phase 1: ORCA Inputs/Outputs
- **Inputs**: Contains `.inp` files for geometry optimization and frequency calculations of HCl, DCl, CO, and NO. Includes a PES scan for HCl.
- **Outputs**: Directory for storing ORCA log files.

### 2. Analysis & Modeling (`2_analysis_modeling/`)
Phase 2: Python Scripts
- `morse_fit.py`: Fits the Potential Energy Surface (PES) data to a Morse potential.
- `reduced_mass.py`: Calculates reduced masses for the diatomic molecules.
- `plots/`: Directory for storing generated plots.

### 3. Molecular Dynamics (`3_molecular_dynamics/`)
Phase 3: GROMACS
- `topology/`: Contains topology files (`.top`).
- `parameters/`: Contains molecular dynamics parameter files (`.mdp`).
- `analysis/`: Python scripts for post-simulation analysis (e.g., FFT).

## Dependencies
See `requirements.txt` for Python dependencies.
- numpy
- pandas
- matplotlib
- scipy

## Usage
1. **Quantum Calculations**: Run ORCA input files in `1_quantum_mechanics/inputs/`.
2. **Analysis**: Use scripts in `2_analysis_modeling/` to analyze quantum chemical data.
3. **MD Simulations**: Use files in `3_molecular_dynamics/` to run GROMACS simulations.
