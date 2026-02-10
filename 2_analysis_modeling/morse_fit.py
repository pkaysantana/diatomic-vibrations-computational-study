
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import re

def morse_potential(r, De, a, re_dist, E_inf):
    """
    V(r) = De * (1 - exp(-a * (r - re)))^2 + E_inf
    """
    return De * (1 - np.exp(-a * (r - re_dist)))**2 + E_inf

def parse_orca_scan(filename):
    """
    Parses an ORCA output file for a Relaxed Surface Scan.
    Returns distances (Angstrom) and energies (Hartree).
    """
    distances = []
    energies = []
    
    # Regex to find the "Scan" data block in ORCA output
    # Note: This is an approximation. Real parsing might need to be more robust depending on ORCA version.
    # We'll look for the final "Surface Scan" table usually printed at the end.
    
    # A simple fallback for this study: manual data entry or reading a formatted .dat file?
    # Let's try to parse the standardized output if possible. 
    # ORCA relaxed scan steps often look like:
    # "The Calculated Surface using the 'Actual' Geometry"
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        reading_scan = False
        for line in lines:
            if "The Calculated Surface using the 'Actual' Geometry" in line:
                reading_scan = True
                continue
                
            if reading_scan:
                if len(line.strip()) == 0:
                    continue
                parts = line.split()
                # Check if line is numeric data (dist, energy)
                try:
                    d = float(parts[0])
                    e = float(parts[1])
                    distances.append(d)
                    energies.append(e)
                except ValueError:
                    # Header lines or end of block
                    if len(distances) > 0: 
                        break # Stop if we hit non-numbers after reading data
                    pass
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return np.array([]), np.array([])
        
    return np.array(distances), np.array(energies)

def main():
    if len(sys.argv) < 2:
        print("Usage: python morse_fit.py <orca_output_file>")
        print("Example: python morse_fit.py ../1_quantum_mechanics/outputs/HCl_PES_Scan.out")
        
        # Fallback dummy data for testing if no file provided
        print("\n--- DEMO MODE (No input file) ---")
        r_data = np.linspace(0.8, 2.5, 20)
        # Fake Morse parameters: De=0.17 H, a=1.8, re=1.275, E_inf=-460.1
        dummy_E = morse_potential(r_data, 0.17, 1.8, 1.275, -460.1) + np.random.normal(0, 0.001, len(r_data))
        fit_morse(r_data, dummy_E, "HCl (Demo)")
        return

    filename = sys.argv[1]
    print(f"Parsing {filename}...")
    r_data, E_data = parse_orca_scan(filename)
    
    if len(r_data) == 0:
        print("No scan data found in file. Ensure it is a valid ORCA Relaxed Scan output.")
        return

    fit_morse(r_data, E_data, filename)

def fit_morse(r_data, E_data, label):
    # Initial guesses:
    # De (depth) ~ range of E
    # re (equilibrium) ~ r at min E
    # E_inf (asymptote) ~ max E
    # a (width) ~ 1.0
    
    E_min = np.min(E_data)
    E_max = np.max(E_data)
    r_min_idx = np.argmin(E_data)
    re_guess = r_data[r_min_idx]
    De_guess = E_max - E_min
    E_inf_guess = E_min # Offset, actually the bottom of the well in the function is E_inf if we don't subtract De. 
    # Wait, form is De(1-exp)^2 + E_inf. At r=re, V=0 + E_inf. So E_inf is the min energy.
    # As r->inf, V -> De + E_inf.
    
    E_inf_guess = E_min
    De_guess = E_max - E_min # Aprx depth
    
    p0 = [De_guess, 2.0, re_guess, E_inf_guess]
    
    try:
        popt, pcov = curve_fit(morse_potential, r_data, E_data, p0=p0, maxfev=10000)
    except RuntimeError:
        print("Fit failed to converge.")
        return

    De, a, re_dist, E_inf = popt
    
    print("\n--- Morse Potential Fit Results ---")
    print(f"De (Well Depth): {De:.6f} Hartrees")
    print(f"a  (Width):      {a:.6f} Angstrom^-1")
    print(f"re (Eq. Bond):   {re_dist:.6f} Angstrom")
    print(f"E0 (Min Energy): {E_inf:.6f} Hartrees")
    
    # Convert spectroscopic constants
    # De in cm-1 = De_hartree * 219474.6
    # k (Force Constant) = 2 * De * a^2 (derived from second derivative at re)
    # But units! De in Hartree, a in 1/Angstrom, r in Angstrom.
    # V'' = 2 * De * a^2  (Hartree / Angstrom^2)
    
    hartree_to_joule = 4.35974e-18
    angstrom_to_meter = 1e-10
    amu_to_kg = 1.66054e-27
    c = 2.9979e10 # cm/s
    h = 6.626e-34
    
    k_hartree_ang = 2 * De * (a**2)
    k_SI = k_hartree_ang * (hartree_to_joule / (angstrom_to_meter**2))
    
    print(f"\nForce Constant (k): {k_SI:.4f} N/m")
    
    # Plotting
    r_fit = np.linspace(min(r_data)*0.9, max(r_data)*1.1, 100)
    E_fit = morse_potential(r_fit, *popt)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(r_data, E_data, color='red', label='ORCA Data')
    plt.plot(r_fit, E_fit, 'b--', label=f'Morse Fit (re={re_dist:.3f} A)')
    plt.xlabel('Bond Length ($\AA$)')
    plt.ylabel('Energy (Hartree)')
    plt.title(f'Morse Potential Fit: {label}')
    plt.legend()
    plt.grid(True)
    
    plot_filename = f"plots/morse_fit_{label.replace('.out','').replace('/','_')}.png"
    plt.savefig(plot_filename)
    print(f"Plot saved to {plot_filename}")

if __name__ == "__main__":
    main()
