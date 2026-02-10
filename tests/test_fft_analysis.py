
import unittest
import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import using SourceFileLoader because the module name has no .py extension in the path usage usually,
# but here it is deeply nested. Let's use the robust method for nested imports if not a package.
# Actually, since we added '..' to sys.path, we can try importing if it were a package, but it's not.
# We will stick to SourceFileLoader for the specific file.
from importlib.machinery import SourceFileLoader
fft_analysis = SourceFileLoader("fft_analysis", "3_molecular_dynamics/analysis/fft_analysis.py").load_module()

class TestFFTPhysics(unittest.TestCase):
    def test_frequency_conversion(self):
        """Test that a 1 ps period wave (1 THz) corresponds to ~33.36 cm-1"""
        # Create a time array with 0.01 ps steps (high res)
        t = np.linspace(0, 100, 10000) # 100 ps
        dt = t[1] - t[0]
        
        # Create a sine wave with frequency 1 THz (period 1 ps)
        # y = A * sin(2*pi*f*t) -> f=1
        # The function expects bond length in nm. 
        # Mean doesn't matter as it removes DC.
        signal = 0.12 + 0.005 * np.sin(2 * np.pi * 1.0 * t)
        
        # Calculate
        wavenumbers, intensity = fft_analysis.calculate_spectrum(t, signal)
        
        # Find peak frequency
        peak_idx = np.argmax(intensity)
        peak_freq_cm = wavenumbers[peak_idx]
        
        # 1 THz = 33.356 cm-1
        self.assertAlmostEqual(peak_freq_cm, 33.356, delta=2.0)

if __name__ == '__main__':
    unittest.main()
