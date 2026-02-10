# Computational Study of Diatomic Vibrations: HCl, DCl, CO, NO

**Author:** [Your Name]
**Date:** [Date]

## Abstract

A multi-scale computational study investigating the vibrational properties of diatomic molecules (HCl, DCl, CO, NO). By combining quantum mechanical calculations (B3LYP/def2-TZVP) with classical molecular dynamics simulations (GROMACS), we evaluate the effects of isotopic substitution and bond anharmonicity.

## 1. Introduction

Vibrational spectroscopy provides deep insights into the nature of chemical bonds. This study aims to:

1. Quantify the isotope effect by comparing HCl and DCl.
2. Map the Potential Energy Surface (PES) of HCl using ab initio methods.
3. Derive vibrational spectra from MD trajectories via Fast Fourier Transform (FFT).

## 2. Methodology

### 2.1 Quantum Mechanics (ORCA)

Electronic structure calculations were performed using **ORCA v5.x**.

- **Level of Theory**: B3LYP hybrid functional.
- **Basis Set**: def2-TZVP (Triple-Zeta Valence Polarized).
- **Hardware Acceleration**: Parallelized across 12 CPU cores (AMD Ryzen).
- **Radical Treatment**: Unrestricted Kohn-Sham (UKS) formalism for NO.

### 2.2 Potential Energy Surface Fitting

The PES of HCl was scanned along the bond axis. The energy data points were fitted to a Morse potential:
$$ V(r) = D_e (1 - e^{-a(r-r_e)})^2 $$
Spectroscopic constants ($D_e$, $k$, $r_e$) were derived from the fit parameters.

### 2.3 Molecular Dynamics (GROMACS)

MD simulations were conducted using **GROMACS 2023+**.

- **Hardware Acceleration**: NVIDIA RTX 5070 Ti (GPU offloading for non-bonded, PME, and bonded interactions).
- **Ensemble**: NVT (Constant Number, Volume, Temperature) at 300K.
- **Integrator**: Leap-frog with a time step of 0.5 fs.
- **Analysis**: Bond length fluctuations were extracted and processed via FFT to obtain the power spectrum.

## 3. Results and Discussion

### 3.1 Reduced Mass Calculations

| Molecule | Reduced Mass (amu) | Theoretical Freq Ratio |
|----------|-------------------|------------------------|
| HCl      | 0.98              | 1.00                   |
| DCl      | 1.90              | ~0.72                  |
| CO       | 6.86              | -                      |
| NO       | 7.47              | -                      |

### 3.2 Quantum Mechanical Results

*Insert ORCA optimization results here (Bond lengths, Harmonic Frequencies).*

- **HCl**: ...
- **DCl**: ...

### 3.3 Morse Potential Fit

![Morse Potential Fit](../2_analysis_modeling/plots/morse_fit_HCl_PES_Scan.png)
*Figure 1: Morse potential fit for HCl.*

**Derived Parameters:**

- Well Depth ($D_e$): ...
- Force Constant ($k$): ...

### 3.4 Molecular Dynamics & FFT

![FFT Spectrum](../3_molecular_dynamics/analysis/fft_spectrum.png)
*Figure 2: Vibrational spectrum derived from MD trajectory.*

The peak position corresponds to the fundamental vibrational frequency ($\nu$).

## 4. Conclusion

[Summarize whether the MD results align with QM predictions and literature values.]
