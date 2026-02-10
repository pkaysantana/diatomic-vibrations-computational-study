
import unittest
import numpy as np
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from importlib.machinery import SourceFileLoader
morse_fit = SourceFileLoader("morse_fit", "2_analysis_modeling/morse_fit.py").load_module()

class TestMorsePotential(unittest.TestCase):
    def test_potential_at_equilibrium(self):
        """At r = re, V(r) should be E_inf (the vertical shift)"""
        De = 0.17
        a = 2.0
        re = 1.28
        E_inf = -100.0
        
        # When r = re, (1 - exp(0))^2 = (1-1)^2 = 0. So V = 0 + E_inf
        result = morse_fit.morse_potential(re, De, a, re, E_inf)
        self.assertAlmostEqual(result, E_inf, places=6)

    def test_potential_at_infinity(self):
        """At r -> infinity, V(r) should approach De + E_inf"""
        De = 0.17
        a = 2.0
        re = 1.28
        E_inf = -100.0
        r_large = 100.0 # Effectively infinity for this steepness
        
        # exp(-large) -> 0. (1-0)^2 = 1. V -> De + E_inf
        expected = De + E_inf
        result = morse_fit.morse_potential(r_large, De, a, re, E_inf)
        self.assertAlmostEqual(result, expected, places=4)

if __name__ == '__main__':
    unittest.main()
