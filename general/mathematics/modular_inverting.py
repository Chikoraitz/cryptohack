"""
Calculate the modular arithmetic inverse of an element
"""
import sys
from euclid_algorithm import gcd
from extended_gcd import blankinship_algorithm

def multiplicative_inverse(g: int, p: int, verbose: bool = False) -> int:
    """
    We can work within a finite field F_p, including adding and multiplying elements,
    and always obtain another element of the field. 
    For all elements g in the field, there exists a unique integer d, such that: 
    -> g⋅d ≡ 1 mod p.
    This is the multiplicative inverse of g. The multiplicative inverse of g mod p, 
    exists if, and only if, g and p are coprime.
    """
    try:
        if gcd(g,p) != 1:
            raise ValueError
    except ValueError:
        print(f"There is no modular multiplicate inverse of {g} mod {p} because {g} and {p} are not coprime.")
        
    """
    If we know p is prime, then we can apply Fermat's little theorem to find the inverse.
    https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
    """
    
    """
    The general case is to calculate the linear coefficients with the extended euclidean algorithm
    or the blankinship algorithm.
    -> g⋅x + p⋅y = gcd(g, p)  # g and p are coprime, so gcd(g, p) = 1
    -> g⋅x + p⋅y = 1          # By applying modulo p to both sides, we can remove the p⋅y term since it will always be 0 under mod p
    -> g⋅x (mod p) = 1 (mod p)
    -> g⋅x ≡ 1 mod p
    """        
    matrix: tuple = blankinship_algorithm(((g,1,0), (p,0,1)), verbose)
    row: int = matrix[1] if matrix[0][0] == 0 else matrix[0]
    
    d: int = row[1] if row[1] > 0 else row[1] + p
           
    return d
    


if __name__ == "__main__":                
    assert len(sys.argv) == 3, "This script requires two arguments: g element of finite field F_p and p"
    
    try:
        g: int = int(sys.argv[1])
        p: int = int(sys.argv[2])       
    except ValueError:
        print("The script only accepts integers")
    
    assert multiplicative_inverse(g=3, p=5) == 2, f"g^-1 = {multiplicative_inverse(g=3, p=5, verbose=True)}"
    assert multiplicative_inverse(g=7, p=11) == 8, f"g^-1 = {multiplicative_inverse(g=7, p=11, verbose=True)}"
    
    print(f"For 3 ⋅ d ≡ 1 mod 13, d = {multiplicative_inverse(g, p)}")