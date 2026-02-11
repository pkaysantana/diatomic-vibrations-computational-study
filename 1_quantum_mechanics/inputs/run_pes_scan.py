import os
import subprocess
import numpy as np

# Configuration
ORCA_BIN = os.environ.get("ORCA_BIN", "orca") # Will fallback to 'orca' if not set
TEMPLATE = """! DLPNO-CCSD(T) cc-pVQZ cc-pVQZ/C TightSCF
%pal nprocs 8 end
%maxcore 5000
* xyz 0 1
H 0 0 0
Cl 0 0 {dist:.4f}
*
"""

DISTANCES = np.linspace(0.8, 4.0, 21)
OUTPUT_FILE = "../outputs/HCl_PES_Scan.out"

def run_scan():
    print(f"Starting Manual PES Scan: 21 points, 0.8 to 4.0 Angstroms")
    print(f"Theory: DLPNO-CCSD(T)/cc-pVQZ")
    
    # Clear output file
    with open(OUTPUT_FILE, 'w') as f:
        f.write("MANUAL PES SCAN START\n")

    for r in DISTANCES:
        print(f"  Calculating Point: r = {r:.4f} A ...")
        
        # Write Input
        inp_content = TEMPLATE.format(dist=r)
        with open("HCl_PES_Point.inp", 'w') as f:
            f.write(inp_content)
            
        # Run ORCA
        # We catch explicit path from environment or assume it's in PATH
        # run_antigravity.sh exports ORCA_DIR to PATH, so 'orca' should work
        # providing absolute path logic in python is also good
        
        cmd = ["orca", "HCl_PES_Point.inp"]
        # If absolute path needed and not in PATH, checking a common var
        if os.path.exists(os.environ.get("ORCA_FULL_PATH", "")):
             cmd[0] = os.environ["ORCA_FULL_PATH"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout
        except subprocess.CalledProcessError as e:
            print(f"    Error at r={r:.4f}: {e}")
            output = e.stdout + "\n" + e.stderr
            
        # Append to master output with markers for benchmark_compare.py
        with open(OUTPUT_FILE, 'a') as f:
            f.write(f"\nDISTANCE: {r:.4f}\n")
            f.write(output)
            f.write("\n------------------------------------------------\n")

    print("Manual PES Scan Complete.")

if __name__ == "__main__":
    run_scan()
