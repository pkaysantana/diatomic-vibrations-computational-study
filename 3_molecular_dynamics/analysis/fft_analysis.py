import numpy as np
import matplotlib.pyplot as plt

# 1. Load your bond length data 
# (You'll generate this using: gmx distance -s nvt.tpr -f nvt.trr -o dist.xvg)
try:
    data = np.loadtxt('dist.xvg', comments=['#', '@'])
except OSError:
    print("Error: 'dist.xvg' not found. Please generate it first using 'gmx distance -s nvt.tpr -f nvt.trr -o dist.xvg'")
    exit(1)

if data.size == 0:
    print("Error: 'dist.xvg' is empty.")
    exit(1)

# Handle cases where dist.xvg might have multiple columns or different formatting
# GMX distance usually outputs: time, dist check
if len(data.shape) > 1:
    time = data[:, 0]    # Time in ps
    dist = data[:, 1]    # Distance in nm
else:
    # Fallback or error if format is unexpected
    print("Unexpected data format in dist.xvg")
    exit(1)

# 2. Perform Fast Fourier Transform (FFT)
dt = time[1] - time[0]
n = len(dist)
dist_detrend = dist - np.mean(dist) # Remove DC offset
fft_vals = np.fft.rfft(dist_detrend)
freqs = np.fft.rfftfreq(n, d=dt)

# 3. Convert Frequency to Wavenumber (cm-1)
# 1 ps^-1 = 33.356 cm^-1
wavenumbers = freqs * 33.3564

plt.figure(figsize=(10, 5))
plt.plot(wavenumbers, np.abs(fft_vals))
plt.xlim(0, 4000) # Region for HCl/CO vibrations
plt.xlabel('Wavenumber (cm$^{-1}$)')
plt.ylabel('Intensity')
plt.title('Vibrational Spectrum derived from MD Trajectory')
plt.grid(True)
plt.savefig('fft_spectrum.png')
print("Spectrum saved as fft_spectrum.png")
plt.show()
