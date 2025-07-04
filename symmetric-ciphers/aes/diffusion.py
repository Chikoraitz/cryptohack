"""
How AES Works
Diffusion through Permutation
---
"""
from matrix import ByteMatrix, array2matrix, matrix2array

def shift_rows(s: ByteMatrix):
    # In Python, arguments are described to functions as "pass-by-object-reference" or "pass-by-sharing"
    # If the object is mutable (e.g., a list or dictionary), changes made through the parameter will 
    #  affect the original object
    # However, if the object is immutable (e.g., a number, string, or tuple) any modifications made to 
    #  the parameter within the function will not affect the original object, as the parameter will be
    #  reassigned to a new object.
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def inv_shift_rows(s: ByteMatrix):
    # Row-notation
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]


xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def mix_single_column(a: bytearray):
    # see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)


def mix_columns(s: ByteMatrix):
    for i in range(4):
        mix_single_column(s[i])


def inv_mix_columns(s: ByteMatrix):
    # see Sec 4.1.3 in The Design of Rijndael
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    mix_columns(s)


if __name__ == "__main__":
    state: list[list[int]] = [
        [108, 106, 71, 86],
        [96, 62, 38, 72],
        [42, 184, 92, 209],
        [94, 79, 8, 54],
    ]
    
    inv_mix_columns(state)
    inv_shift_rows(state)
    
    print(bytes(matrix2array(state)))
    
