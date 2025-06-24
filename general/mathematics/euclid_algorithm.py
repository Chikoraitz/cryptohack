"""

"""

import sys

def gcd(a, b, verbose=False):
    # Take the larger of the two numbers
    if a > b:
        larger = a
        smaller = b
    else:
        larger = b
        smaller = a
    
    # larger = smaller * q + r
    q = larger // smaller
    r = larger % smaller
    
    if verbose:
        print(f"{larger} = {smaller} * {q} + {r}")
        
    # If the remainder is zero, the result is the last iteration remainder
    if r == 0:
        return smaller
    else:
        # Else execute the algorithm again with the quotient and remainder
        return gcd(smaller, r, verbose)
    
    
if __name__ == "__main__":
    assert len(sys.argv) == 3, "This script requires two arguments for calculating their gcd"
    assert gcd(12, 8) == 4, gcd(12, 8)
    assert gcd(11, 17) == 1, gcd(11, 17)
    assert gcd(270, 192) == 6, gcd(270, 192)
    assert gcd(36, 60) == 12, gcd(36, 60)
    
    print(f"gcd({sys.argv[1]}, {sys.argv[2]}) = {gcd(int(sys.argv[1]), int(sys.argv[2]))}")