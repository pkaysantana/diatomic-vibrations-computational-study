
import sys

def calculate_reduced_mass(m1, m2):
    """Calculates reduced mass in AMU."""
    return (m1 * m2) / (m1 + m2)

def main():
    # Atomic masses in AMU (Protons + Neutrons roughly, or averaged)
    masses = {
        'H': 1.00784,
        'D': 2.014102,
        'C': 12.011,
        'N': 14.007,
        'O': 15.999,
        'Cl35': 34.968853, # Main isotope for study
        'Cl': 35.453       # Average
    }
    
    pairs = [
        ('H', 'Cl35', 'HCl'),
        ('D', 'Cl35', 'DCl'),
        ('C', 'O', 'CO'),
        ('N', 'O', 'NO')
    ]
    
    print(f"{'Molecule':<10} | {'Reduced Mass (AMU)':<20} | {'Reduced Mass (kg)':<20}")
    print("-" * 56)
    
    amu_to_kg = 1.66054e-27
    
    for a1, a2, name in pairs:
        mu_amu = calculate_reduced_mass(masses[a1], masses[a2])
        mu_kg = mu_amu * amu_to_kg
        print(f"{name:<10} | {mu_amu:<20.6f} | {mu_kg:<20.4e}")

if __name__ == "__main__":
    main()
