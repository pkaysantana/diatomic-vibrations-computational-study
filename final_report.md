# Computational Study of Diatomic Vibrations: HCl, DCl, CO, NO

**Author:** Don Aborah
**Date:** 10/02/2026
**Hardware:** AMD Ryzen 9 9955HX (12 Cores for ORCA) | NVIDIA RTX 5070 Ti (GROMACS GPU offload)

## Abstract

A multi-scale computational study investigating the vibrational properties of diatomic molecules (HCl, DCl, CO, NO). By combining high-accuracy quantum mechanical calculations (DLPNO-CCSD(T)/cc-pVQZ) with classical molecular dynamics simulations (GROMACS), we evaluate the effects of isotopic substitution and bond anharmonicity. The study successfully achieved "gold standard" accuracy for the HCl Potential Energy Surface.

## 1. Introduction

Vibrational spectroscopy provides deep insights into the nature of chemical bonds. This study aims to:

1. Quantify the isotope effect by comparing HCl and DCl.
2. Map the Potential Energy Surface (PES) of HCl using ab initio methods (DLPNO-CCSD(T)).
3. Derive vibrational spectra from MD trajectories via Fast Fourier Transform (FFT).

## 2. Methodology

### 2.1 Quantum Mechanics (ORCA)

Electronic structure calculations were performed using **ORCA v6.1.0**.

- **Geometry Optimization**: PBE0/def2-TZVP.
- **High-Accuracy PES**: DLPNO-CCSD(T) with the cc-pVQZ basis set (Correlation Consistent Quadruple Zeta) for near-CBS limit accuracy.
- **Hardware Acceleration**: Parallelised across 12 CPU cores.
- **Scan Method**: Robust manual PES scan loop (21 points, 0.8Å - 4.0Å) to bypass internal driver limitations.

### 2.2 Potential Energy Surface Fitting

The PES of HCl was scanned along the bond axis. The energy data points were fitted to a Morse potential:
$$ V(r) = D_e (1 - e^{-a(r-r_e)})^2 $$

### 2.3 Molecular Dynamics (GROMACS)

MD simulations were conducted using **GROMACS 2023+**.

- **Hardware Acceleration**: NVIDIA RTX 5070 Ti (GPU offloading for non-bonded, PME, and bonded interactions).
- **Ensemble**: NVT at 300K.
- **Integrator**: Leap-frog with a time step of 0.5 fs.
- **Analysis**: FFT of bond length fluctuations.

## 3. Results and Discussion

### 3.1 Vibrational Frequencies (Benchmark)

The calculated fundamental frequencies show excellent agreement with experimental NIST data.

| Molecule | Calc Freq (cm⁻¹) | Exp Freq (NIST) | % Error | Note |
|----------|-----------------|-----------------|---------|------|
| **DCl**  | 2107.9          | 2091.0          | **0.81%** | Very High Accuracy |
| **HCl**  | 2938.3          | 2885.9          | **1.82%** | High Accuracy |
| **CO**   | 2212.6          | 2143.0          | 3.25%   | Harmonic Approx |
| **NO**   | 1975.5          | 1876.0          | 5.30%   | Open Shell System |

### 3.2 Isotope Effect (HCl vs DCl)

The reduced mass effect is clearly observed.

- Theoretical Frequency Ratio (HCl/DCl) ≈ $\sqrt{\mu_{DCl}/\mu_{HCl}} \approx 1.39$
- Calculated Ratio: $2938.3 / 2107.9 = 1.393$
- This confirms the harmonic oscillator prediction for isotopic substitution.

### 3.3 Morse Potential Fit (DLPNO-CCSD(T)/cc-pVQZ)

The use of Coupled Cluster theory provided a smooth, highly accurate potential energy surface.

![Morse Potential Fit](../2_analysis_modeling/plots/morse_fit_HCl_PES_Scan.png)
*Figure 1: High-Accuracy Morse potential fit for HCl.*

### 3.4 Molecular Dynamics & FFT

The classical MD simulations, accelerated by the RTX 5070 Ti, yielded stable trajectories. The FFT analysis recovered the fundamental frequencies with <2% error for the hydrogen halides, demonstrating the validity of the force field parameters derived from the quantum data.

![FFT Spectrum](../3_molecular_dynamics/analysis/fft_spectrum.png)
*Figure 2: Vibrational spectrum derived from MD trajectory.*

## 4. Conclusion

The computational pipeline successfully integrated high-level quantum theory (DLPNO-CCSD(T)) with efficient GPU-accelerated molecular dynamics. The results (0.81% error for DCl) demonstrate that this multi-scale approach achieves research-grade accuracy on a workstation setup.
