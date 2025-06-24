"""
How AES Works
Round Keys
---
"""
from matrix import ByteMatrix, array2matrix, matrix2array

def add_round_key(s: ByteMatrix, k: ByteMatrix) -> None:
    """Iterates over the AES 4x4 matrix state and adds the round key.
    Returns a 4x4 matrix.
    """
    s_vector: bytearray = matrix2array(s)
    key: bytearray = matrix2array(k)
    s[:] = array2matrix([state_elem ^ key[index] for index, state_elem in enumerate(s_vector)])


if __name__ == "__main__":
    state = [
        [206, 243, 61, 34],
        [171, 11, 93, 31],
        [16, 200, 91, 108],
        [150, 3, 194, 51],
    ]

    round_key = [
        [173, 129, 68, 82],
        [223, 100, 38, 109],
        [32, 189, 53, 8],
        [253, 48, 187, 78],
    ]

    add_round_key(state, round_key)
    assert state == [[99, 114, 121, 112], [116, 111, 123, 114], [48, 117, 110, 100], [107, 51, 121, 125]], state
    
    print(bytes(matrix2array(state)))

