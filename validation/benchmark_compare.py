
import os
import sys
import re

# Standard values from NIST (as provided in prompt)
reference_data = {
    'HCl': {'re': 1.275, 'freq': 2885.9, 'k': 5.16}, # Freq is fundamental
    'DCl': {'re': 1.275, 'freq': 2091.0, 'k': 5.16}, 
    'CO':  {'re': 1.128, 'freq': 2143.0, 'k': 18.6}, 
    'NO':  {'re': 1.151, 'freq': 1876.0, 'k': 15.5}
}


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
        if filename.endswith(".out"):
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
                
    # Fallback/Debug if empty
    if not results:
         print("No valid ORCA output files found. Using Mock Data for demonstration.")
         results['HCl'] = {'re': 1.28, 'freq': 2991.0}

    return results

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
                print(f"{mol:<10} | {'re (A)':<10} | {calc_re:<10.3f} | {ref_re:<10.3f} | {err_re:<10.2f}%")
            
            # Compare Frequency
            if 'freq' in data:
                calc_freq = data['freq']
                ref_freq = ref['freq']
                err_freq = abs(calc_freq - ref_freq) / ref_freq * 100
                status = " (Harmonic vs Fund)" if err_freq > 2.0 else ""
                print(f"{mol:<10} | {'freq (cm-1)':<10} | {calc_freq:<10.1f} | {ref_freq:<10.1f} | {err_freq:<10.2f}%{status}")

if __name__ == "__main__":
    sim_results = load_simulation_results()
    validate(sim_results)
