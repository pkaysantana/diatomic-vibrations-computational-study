
import os
import numpy as np

# Mock Data Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
qm_output_dir = os.path.join(base_dir, '1_quantum_mechanics', 'outputs')
md_analysis_dir = os.path.join(base_dir, '3_molecular_dynamics', 'analysis')
pes_scan_file = os.path.join(qm_output_dir, 'HCl_PES_Scan.out')

os.makedirs(qm_output_dir, exist_ok=True)
os.makedirs(md_analysis_dir, exist_ok=True)

# 1. Mock ORCA Outputs
molecules = {
    'HCl': {'freq': 2885.9, 're': 1.275, 'e': -460.1},
    'DCl': {'freq': 2091.0, 're': 1.275, 'e': -460.1}, 
    'CO':  {'freq': 2143.0, 're': 1.128, 'e': -113.3},
    'NO':  {'freq': 1876.0, 're': 1.151, 'e': -129.9}
}

for mol, data in molecules.items():
    filepath = os.path.join(qm_output_dir, f"{mol}.out")
    print(f"Generating mock {mol}.out...")
    with open(filepath, 'w') as f:
        f.write(f"""
        ************************************************************
        *                        ORCA 5.0.3                        *
        *           Neese Group - Max Planck Institute             *
        ************************************************************
        
        FINAL SINGLE POINT ENERGY      {data['e']:.6f}
        
        -----------------------
        INTERATOMIC DISTANCES
        -----------------------
        R(H  ,Cl )   {data['re']:.4f}  Angstrom

        -----------------------
        VIBRATIONAL FREQUENCIES
        -----------------------
           0:         0.00 cm**-1
           1:         0.00 cm**-1
           2:         0.00 cm**-1
           3:         0.00 cm**-1
           4:         0.00 cm**-1
           5:         0.00 cm**-1
           6:      {data['freq']:.2f} cm**-1
           
        NORMAL MODES
        ...
        """)

# 2. Mock GROMACS dist.xvg (Sine Wave + Noise)
# HCl freq ~ 2885 cm^-1 -> ~86.5 THz -> Period ~ 0.011 ps
# We need check sampling rate (dt=0.002 ps is standard)
print("Generating mock dist.xvg for FFT analysis...")
time = np.arange(0, 10, 0.002) # 10 ps, 5000 steps
freq_thz = 2885.0 / 33.356 # ~86.5 THz
bond_length = 0.1275 + 0.005 * np.sin(2 * np.pi * freq_thz * time) + 0.001 * np.random.normal(size=len(time))

with open(os.path.join(md_analysis_dir, 'dist.xvg'), 'w') as f:
    f.write("@    title \"Bond Distance\"\n")
    f.write("@    xaxis  label \"Time (ps)\"\n")
    f.write("@    yaxis  label \"Distance (nm)\"\n")
    for t, r in zip(time, bond_length):
        f.write(f"{t:.5f}  {r:.5f}\n")

# 3. Mock PES Scan Output
print("Generating mock HCl_PES_Scan.out for Morse Fit...")
r_scan = np.linspace(0.8, 4.0, 20)
# Morse Potential: D_e * (1 - exp(-a*(r-re)))^2
De = 0.17 # Hartrees roughly
a = 1.0
re_scan = 1.275
energies = -460.0 + De * (1 - np.exp(-a * (r_scan - re_scan)))**2

with open(pes_scan_file, 'w') as f:
    f.write("ORCA PES SCAN OUTPUT MOCK\n")
    f.write("The Calculated Surface using the 'Actual' Geometry\n")
    for r, e in zip(r_scan, energies):
        f.write(f"   {r:.4f}      {e:.8f}\n")
    f.write("\n")

print("Mock data generation complete.")
