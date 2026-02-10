
import os

# Molecular properties for MD Setup
# Bond Length (nm), Force Constant (kJ/mol/nm^2), Atomic Masses (amu)
# k (N/m) -> kJ/mol/nm^2: 1 N/m = 1 J/m^2 = 1e-3 kJ / (1e-18 m^2) ??
# No.
# k [N/m] = [J/m^2]. 
# GROMACS units: kJ/mol/nm^2.
# 1 N/m = 1 J/m^2 = (1/1000 kJ) / (1e-9 nm)^2 = 1e-3 / 1e-18 = 1e15 kJ/m^2? No.
# Let's use standard conversion.
# k_SI [N/m]. 
# k_GMX = k_SI * 0.0006022 * 1000 / 2 ?? -> 1/2 factor is in GROMACS functional form?
# GROMACS Harmonic Potential: V(r) = 1/2 k (r - b0)^2. 
# So we insert k directly.
# N/m to kJ/mol/nm^2:
# 1 N/m = 1 (kg m/s^2)/m = 1 kg/s^2.
# 1 kJ/mol/nm^2 = 1000 J / 6.022e23 / (1e-9 m)^2 = 1000 / 6.022e23 / 1e-18 J/m^2
# = 1e21 / 6.022e23 = 1.66e-3 J/m^2.
# So 1 N/m = 6.022e2 / 1 = 602.2 kJ/mol/nm^2.
# NIST/Experimental k values are usually ~500-2000 N/m.
# So k_GMX should be ~300,000 - 1,200,000.

# NIST Reference Data (approx)
# HCl: k=516 N/m -> ~310,000
# CO: k=1860 N/m -> ~1,120,000
# NO: k=1550 N/m -> ~933,000
# DCl: k=516 N/m (Same force constant, different mass)

molecules_data = {
    'HCl': {'r0': 0.1275, 'k': 310000, 'at1': 'H', 'm1': 1.008, 'at2': 'Cl', 'm2': 35.45},
    'DCl': {'r0': 0.1275, 'k': 310000, 'at1': 'D', 'm1': 2.014, 'at2': 'Cl', 'm2': 35.45},
    'CO':  {'r0': 0.1128, 'k': 1120000, 'at1': 'C', 'm1': 12.01, 'at2': 'O', 'm2': 16.00},
    'NO':  {'r0': 0.1151, 'k': 933000,  'at1': 'N', 'm1': 14.01, 'at2': 'O', 'm2': 16.00}
}

base_dir = os.path.dirname(os.path.abspath(__file__))
topology_dir = os.path.join(base_dir, '3_molecular_dynamics', 'topology')
os.makedirs(topology_dir, exist_ok=True)

# Generate Files
for mol, data in molecules_data.items():
    
    # 1. Generate GRO File (Structure)
    gro_file = os.path.join(topology_dir, f"{mol}.gro")
    dist_nm = data['r0']
    
    content_gro = f"{mol} molecule\n"
    content_gro += "    2\n"
    # Residue 1, Name MOL, Atom 1, Number 1, Position...
    content_gro += f"{1:5d}{mol:<5s}{data['at1']:>5s}{1:5d}{0.000:8.3f}{0.000:8.3f}{0.000:8.3f}\n"
    content_gro += f"{1:5d}{mol:<5s}{data['at2']:>5s}{2:5d}{dist_nm:8.3f}{0.000:8.3f}{0.000:8.3f}\n"
    content_gro += f"{4.0:10.5f}{4.0:10.5f}{4.0:10.5f}\n" 
    
    with open(gro_file, "w") as f:
        f.write(content_gro)
    print(f"Generated {gro_file}")

    # 2. Generate TOP File (Topology)
    top_file = os.path.join(topology_dir, f"{mol}.top")
    
    # Simple Topology without include files (Self-contained)
    content_top = f"""; {mol} Topology for Antigravity

[ defaults ]
; nbfunc        comb-rule       gen-pairs       fudgeLJ fudgeQQ
1               2               yes             0.5     0.5

[ atomtypes ]
; name  at.num  mass     charge ptype  sigma      epsilon (Lennard-Jones - generic)
A1       1      {data['m1']:.3f}   0.000  A      0.33       0.00  ; Dummy LJ
A2       17     {data['m2']:.3f}   0.000  A      0.33       0.00  ; Dummy LJ

[ moleculetype ]
; Name            nrexcl
{mol}             3

[ atoms ]
;   nr       type  resnr residue  atom   cgnr     charge       mass
     1         A1      1    {mol}     {data['at1']}      1      0.000      {data['m1']:.3f}
     2         A2      1    {mol}     {data['at2']}      1      0.000      {data['m2']:.3f}

[ bonds ]
;  ai    aj funct            c0            c1 (k)
    1     2     1      {data['r0']:.4f}   {data['k']:.1f}

[ system ]
; Name
{mol} Simulation

[ molecules ]
; Compound        #mols
{mol}             1
"""
    with open(top_file, "w") as f:
        f.write(content_top)
    print(f"Generated {top_file}")

print("MD Input Generation Complete (GRO + TOP).")
