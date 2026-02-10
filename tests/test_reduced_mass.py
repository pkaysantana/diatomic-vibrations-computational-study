
import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from importlib.machinery import SourceFileLoader
reduced_mass = SourceFileLoader("reduced_mass", "2_analysis_modeling/reduced_mass.py").load_module()

class TestReducedMass(unittest.TestCase):
    def test_hcl_mass(self):
        """Test HCl reduced mass calculation against known value ~0.9796 amu"""
        m_H = 1.00784
        m_Cl = 34.968853
        expected = (m_H * m_Cl) / (m_H + m_Cl)
        result = reduced_mass.calculate_reduced_mass(m_H, m_Cl)
        self.assertAlmostEqual(result, expected, places=6)

    def test_symmetry(self):
        """Test that order of masses doesn't matter (m1, m2) == (m2, m1)"""
        m1 = 12.0
        m2 = 16.0
        self.assertEqual(reduced_mass.calculate_reduced_mass(m1, m2), 
                         reduced_mass.calculate_reduced_mass(m2, m1))

if __name__ == '__main__':
    unittest.main()
