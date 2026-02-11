
import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Standard values from NIST
reference_data = {
    'HCl': {'re': 1.275, 'freq': 2885.9, 'k': 5.16}, 
    'DCl': {'re': 1.275, 'freq': 2091.0, 'k': 5.16}, 
    'CO':  {'re': 1.128, 'freq': 2143.0, 'k': 18.6}, 
    'NO':  {'re': 1.151, 'freq': 1876.0, 'k': 15.5}
}

def morse_potential(r, De, a, re):
    return De * (1 - np.exp(-a * (r - re)))**2

def extract_pes_data(filename):
    """
    Parses ORCA PES data. Handles:
    1. Internal ORCA Scan table ('The Calculated Surface')
    2. Concatenated manual loop loop ('DISTANCE:')
    """
    distances = []
    energies = []
    
    if not os.path.exists(filename):
        return distances, energies

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        # Strategy 1: Look for Internal ORCA Scan Table
        in_table = False
        for line in lines:
            if "The Calculated Surface" in line and "Actual Energy" in line:
                in_table = True
                continue
            if in_table:
                if not line.strip() or "---" in line:
                    if len(distances) > 0: break
                    else: continue
                parts = line.split()
                if len(parts) == 2:
                    try:
                        distances.append(float(parts[0]))
                        energies.append(float(parts[1]))
                    except: pass
        
        # Strategy 2: Look for manual Loop markers if Strategy 1 failed
        if not distances:
            current_r = None
            for line in lines:
                if "DISTANCE:" in line:
                    current_r = float(line.split()[1])
                elif "FINAL SINGLE POINT ENERGY" in line and current_r is not None:
                    e = float(line.split()[4])
                    distances.append(current_r)
                    energies.append(e)
                    current_r = None
    except Exception as e:
        print(f"Error reading PES file: {e}")

    return distances, energies

def load_simulation_results():
    """
    Parses the output files from ORCA to extract calculated values.
    """
    results = {}
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_path, '1_quantum_mechanics', 'outputs')

    if not os.path.exists(output_dir):
        print(f"Warning: Output directory {output_dir} not found.")
        return results

    for filename in os.listdir(output_dir):
        if filename.endswith(".out") and "PES" not in filename:
            mol_name = filename.replace(".out", "")
            filepath = os.path.join(output_dir, filename)
            
            data = {}
            with open(filepath, 'r') as f:
                content = f.read()
                
                # Parse Vibrational Frequencies
                if "VIBRATIONAL FREQUENCIES" in content:
                    freq_matches = re.findall(r"\s+(\d+):\s+(\d+\.\d+)\s+cm\*\*-1", content)
                    if freq_matches:
                        freqs = [float(x[1]) for x in freq_matches if float(x[1]) > 10.0]
                        if freqs:
                            data['freq'] = max(freqs)

                # Parse Bond Length
                if "INTERATOMIC DISTANCES" in content:
                    dist_match = re.search(r"R\((\w+)\s*,\s*(\w+)\)\s+(\d+\.\d+)\s+Ang", content)
                    if dist_match:
                        data['re'] = float(dist_match.group(3))
            
            if data:
                results[mol_name] = data

    return results

def plot_pes(distances, energies, mol_name="HCl"):
    if not distances or not energies:
        print("No PES data to plot.")
        return

    # Shift energy to zero minimum
    min_e = min(energies)
    rel_energies = [(e - min_e) * 627.509 for e in energies] # Convert Hartree to kcal/mol
    
    plt.figure(figsize=(8, 6))
    plt.plot(distances, rel_energies, 'bo', label='ORCA Scan (B3LYP)')
    
    # Fit Morse Potential
    try:
        popt, pcov = curve_fit(morse_potential, distances, rel_energies, p0=[100, 2.0, 1.27])
        r_fit = np.linspace(min(distances), max(distances), 100)
        e_fit = morse_potential(r_fit, *popt)
        plt.plot(r_fit, e_fit, 'r-', label=f'Morse Fit (De={popt[0]:.1f} kcal/mol)')
    except:
        print("Morse fit failed.")

    plt.xlabel('Bond Length (Angstrom)')
    plt.ylabel('Potential Energy (kcal/mol)')
    plt.title(f'Potential Energy Surface: {mol_name}')
    plt.legend()
    plt.grid(True)
    
    output_path = f"../2_analysis_modeling/plots/morse_fit_{mol_name}_PES_Scan.png"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(output_path)
    print(f"PES Plot saved to {output_path}")

def validate(results):
    print("\n--- BENCHMARK VALIDATION REPORT ---")
    print(f"{'Molecule':<10} | {'Property':<10} | {'Calc':<10} | {'Exp (NIST)':<10} | {'% Error':<10}")
    print("-" * 65)
    
    for mol, data in results.items():
        if mol in reference_data:
            ref = reference_data[mol]
            
            # Compare Bond Length
            if 're' in data:
                calc_re = data['re']
                ref_re = ref['re']
                err_re = abs(calc_re - ref_re) / ref_re * 100
                # print(f"{mol:<10} | {'re (A)':<10} | {calc_re:<10.3f} | {ref_re:<10.3f} | {err_re:<10.2f}%")
            
            # Compare Frequency
            if 'freq' in data:
                calc_freq = data['freq']
                ref_freq = ref['freq']
                err_freq = abs(calc_freq - ref_freq) / ref_freq * 100
                status = " (Harmonic vs Fund)" if err_freq > 2.0 else ""
                print(f"{mol:<10} | {'freq (cm-1)':<10} | {calc_freq:<10.1f} | {ref_freq:<10.1f} | {err_freq:<10.2f}%{status}")

if __name__ == "__main__":
    # 1. Parse Simulation Results
    sim_results = load_simulation_results()
    validate(sim_results)
    
    # 2. Process PES Scan
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pes_file = os.path.join(base_path, '1_quantum_mechanics', 'outputs', 'HCl_PES_Scan.out')
    
    print(f"\nParsing {pes_file}...")
    d, e = extract_pes_data(pes_file)
    if d and e:
        plot_pes(d, e, "HCl")
    else:
        print("No valid PES scan data found.")
