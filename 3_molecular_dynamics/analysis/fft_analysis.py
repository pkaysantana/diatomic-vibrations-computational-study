import numpy as np
import matplotlib.pyplot as plt
import sys

def calculate_spectrum(time_ps, bond_length_nm):
    """
    Performs FFT on bond length trajectory to obtain vibrational spectrum.
    
    Args:
        time_ps (np.array): Time in picoseconds.
        bond_length_nm (np.array): Bond length in nanometers.
        
    Returns:
        tuple: (wavenumbers_cm1, intensity)
    """
    if len(time_ps) == 0:
        return np.array([]), np.array([])
        
    # 1. Remove DC component (mean centering)
    fluctuation = bond_length_nm - np.mean(bond_length_nm)
    
    # 2. Windowing (Hanning) to reduce spectral leakage
    # Optional but recommended for signal processing
    window = np.hanning(len(fluctuation))
    fluctuation_windowed = fluctuation * window
    
    # 3. FFT
    time_ps = np.array(time_ps)
    bond_length_nm = np.array(bond_length_nm) # Corrected from dist_nm
    if len(time_ps) < 2:
        print("Not enough data for FFT.")
        return np.array([]), np.array([]) # Ensure return type matches function signature
    
    dt = time_ps[1] - time_ps[0]
    n_samples = len(time_ps)
    
    # rfft returns positive frequencies
    fft_vals = np.abs(np.fft.rfft(fluctuation_windowed))
    freqs_ps_inverse = np.fft.rfftfreq(n_samples, d=dt)
    
    # 4. Convert units: ps^-1 -> cm^-1
    # 1 ps^-1 = 33.3564 cm^-1
    wavenumbers = freqs_ps_inverse * 33.3564
    
    return wavenumbers, fft_vals

def main():
    # Load GROMACS data
    xvg_file = "dist.xvg"
    
    try:
        # GROMACS xvg files have headers starting with @ and #
        data = np.loadtxt(xvg_file, comments=["@", "#"])
    except OSError:
        print(f"Error: '{xvg_file}' not found. Please generate it first using 'gmx distance ...'")
        # Exit gracefully so tests don't crash if they import this (though they shouldn't run main)
        return
    except Exception as e:
        print(f"Error reading {xvg_file}: {e}")
        return

    if data.size == 0:
        print(f"Error: '{xvg_file}' is empty.")
        return

    # Handle cases where dist.xvg might have multiple columns
    if len(data.shape) > 1:
        time_ps = data[:, 0]
        bond_length_nm = data[:, 1]
    else:
        print("Unexpected data format in dist.xvg")
        return

    wavenumbers, intensity = calculate_spectrum(time_ps, bond_length_nm)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(wavenumbers, intensity, color='black')
    plt.xlim(0, 4000)
    plt.xlabel(r'Wavenumber ($\text{cm}^{-1}$)')
    plt.ylabel('Intensity (a.u.)')
    plt.title('Vibrational Spectrum from MD Trajectory (FFT)')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    output_file = "fft_spectrum.png"
    plt.savefig(output_file, dpi=300)
    print(f"Spectrum saved to {output_file}")

if __name__ == "__main__":
    main()
