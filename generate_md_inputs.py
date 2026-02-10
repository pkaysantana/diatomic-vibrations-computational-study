
import os

# Molecular properties (approximate bond lengths for starting structures)
molecules = {
    'HCl': 1.27,
    'DCl': 1.27,
    'CO': 1.13,
    'NO': 1.15
}

base_dir = os.path.dirname(os.path.abspath(__file__))
topology_dir = os.path.join(base_dir, '3_molecular_dynamics', 'topology')
os.makedirs(topology_dir, exist_ok=True)

for mol, bond_length in molecules.items():
    gro_file = os.path.join(topology_dir, f"{mol}.gro")
    
    # Calculate atom positions (aligned along x-axis)
    # Atom 1 at origin, Atom 2 at bond_length
    # Format: Residue Number (5d), Residue Name (5s), Atom Name (5s), Atom Number (5d), Position (3f), Velocity (3f)
    # Positions are in nm. Bond length is in Angstrom, so divide by 10.
    
    dist_nm = bond_length / 10.0
    
    # Simple GRO format for diatomic molecule
    content = f"{mol} molecule\n"
    content += "    2\n"
    
    # Atom 1 (e.g., H/C/N)
    atom1 = "H" if "H" in mol else ("C" if "C" in mol else "N")
    # Atom 2 (e.g., Cl/O)
    atom2 = "Cl" if "Cl" in mol else "O"
    
    # Line format: %5d%-5s%5s%5d%8.3f%8.3f%8.3f
    line1 = f"{1:5d}{mol:<5s}{atom1:>5s}{1:5d}{0.000:8.3f}{0.000:8.3f}{0.000:8.3f}\n"
    line2 = f"{1:5d}{mol:<5s}{atom2:>5s}{2:5d}{dist_nm:8.3f}{0.000:8.3f}{0.000:8.3f}\n"
    
    content += line1 + line2
    content += f"{2.0:10.5f}{2.0:10.5f}{2.0:10.5f}\n" # Box size (arbitrary 2nm)
    
    with open(gro_file, "w") as f:
        f.write(content)
    
    print(f"Generated {gro_file}")

print("MD Input Generation Complete.")
