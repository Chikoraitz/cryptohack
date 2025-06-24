"""
The Extended Euclidean Algorithm is used to find the linear combination of a and b 
so that it equals its gcd(a, b). In other words, find u and v so that: a * u + b * v = gcd(a, b)
u and v exist for any pair (a, b) of positive integers - Bezout's Lemma.
"""

import sys
from euclid_algorithm import gcd

assert len(sys.argv) == 3, "This script requires two arguments for calculating their gcd"

# https://math.libretexts.org/Bookshelves/Combinatorics_and_Discrete_Mathematics/Elementary_Number_Theory_(Clark)/01%3A_Chapters/1.09%3A_Blankinship's_Method
def blankinship_algorithm(aug_matrix, verbose=False):
    """
    The problem with the extended Euclidean algorithm is that it needs to keep track of the 
    intermediary values while computing gcd(a,b) and work backwards to find the {u,v} coefficients.
    Better way to find the coefficients, is to use the Blankinship algorithm through an augmented
    matrix, which removes removes the need to keep track of the aforementioned intermediary values, 
    while at the same time producing gcd(a, b).
    """
    # 1st row
    q = (-1) * (aug_matrix[0][0] // aug_matrix[1][0])
    new_aug_matrix = ((
        aug_matrix[0][0] + (q * aug_matrix[1][0]), 
        aug_matrix[0][1] + (q * aug_matrix[1][1]), 
        aug_matrix[0][2] + (q * aug_matrix[1][2])), 
        aug_matrix[1]
    )
    
    if verbose:
        print("--")
        print(f"|{new_aug_matrix[0][0]} | {new_aug_matrix[0][1]} {new_aug_matrix[0][2]}|")
        print(f"|{new_aug_matrix[1][0]} | {new_aug_matrix[1][1]} {new_aug_matrix[1][2]}|")
        print("--")
    
    if new_aug_matrix[0][0] == 0:
        return new_aug_matrix
        
    # 2nd row
    q = (-1) * (new_aug_matrix[1][0] // new_aug_matrix[0][0])
    new_aug_matrix = (
        new_aug_matrix[0], (
        aug_matrix[1][0] + (q * new_aug_matrix[0][0]), 
        aug_matrix[1][1] + (q * new_aug_matrix[0][1]), 
        aug_matrix[1][2] + (q * new_aug_matrix[0][2])) 
    )
    
    if verbose:
        print("--")
        print(f"|{new_aug_matrix[0][0]} | {new_aug_matrix[0][1]} {new_aug_matrix[0][2]}|")
        print(f"|{new_aug_matrix[1][0]} | {new_aug_matrix[1][1]} {new_aug_matrix[1][2]}|")
        print("--")
    
    if new_aug_matrix[1][0] == 0:
        return new_aug_matrix
        
    return blankinship_algorithm(new_aug_matrix, verbose)
    

assert gcd(66528, 52920) == 1512

test_matrix = blankinship_algorithm(((35, 1, 0), (15, 0, 1)))
assert test_matrix[0][0] == gcd(35, 15), f"{test_matrix[0][0]} != {gcd(35, 15)}"
assert test_matrix[0][1] == 1, f"{test_matrix[0][1]} != 1"
assert test_matrix[0][2] == -2, f"{test_matrix[0][2]} != -2"

test_matrix = blankinship_algorithm(((1876, 1, 0), (365, 0, 1)))
assert test_matrix[0][0] == gcd(1876, 365), f"{test_matrix[0][0]} != {gcd(1876, 365)}"
assert test_matrix[0][1] == 136, f"{test_matrix[0][1]} != 136"
assert test_matrix[0][2] == -699, f"{test_matrix[0][2]} != -699"


if __name__ == "__main__":
    a = int(sys.argv[1])
    b = int(sys.argv[2])

    if a > b:
        larger = a
        smaller = b
    else:
        larger = b
        smaller = a
         
    matrix = blankinship_algorithm(((larger,1,0), (smaller,0,1)))
    row = matrix[1] if matrix[0][0] == 0 else matrix[0]
    
    assert row[0] == gcd(a,b), f"{row[0]} != {gcd(a,b, verbose=True)}"
    
    print(f"Linear combination: {larger} * {row[1]} + {smaller} * {row[2]} = {row[0]}")
