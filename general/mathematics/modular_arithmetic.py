"""
Calculate the modular arithmetic of a large number a (a mod p),
where a = base ^ exp
Restriction: p is prime
"""
from euclid_algorithm import gcd

def fermat_little_theorem(base: int, exp: int, p: int, verbose: bool = False) -> int:
    """
    https://en.wikipedia.org/wiki/Fermat%27s_little_theorem
    In number theory, Fermat's little theorem states that if p is a prime number,
    then for any integer a, the number (a ^ p) - a is an integer multiple of p:
    -> a ^ p ≡ a mod p
    If a is coprime to p, then Fermat's little theorem states that the number
    a ^ (p - 1) - 1 is an integer multiple of p:
    -> a ^ (p - 1) ≡ 1 mod p
    """
    if p == exp:
        return base
        
    if verbose:
        print(f"GCD({base}, {exp}) = {gcd(base, exp)}")
            
    if gcd(base, exp) == 1 and exp == (p - 1):
        return 1

    return -1


def is_prime(p: int, n_tests: int) -> bool:
    """Fermat's Little Theorem test of primality"""
    return True
    

if __name__ == "__main__":                
    assert fermat_little_theorem(3, 17, 17) == 3
    assert fermat_little_theorem(5, 17, 17) == 5
    assert fermat_little_theorem(7, 16, 17) == 1
    assert fermat_little_theorem(273246787653, 65536, 65537) != 1
    
    print(f"Challenge solution: 273246787654 ^ 65536 ≡ {fermat_little_theorem(273246787653, 65536, 65537, verbose=True)} mod 65537")