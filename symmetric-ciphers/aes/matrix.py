"""
How AES Works
Structure of AES.
---
"""
type ByteMatrix = bytearray[bytearray]

def array2matrix(msg: bytearray) -> ByteMatrix:
    """ Converts a 16-byte vector into a 4x4 matrix.  """
    return [list(msg[i:i+4]) for i in range(0, len(msg), 4)]


def matrix2array(matrix: ByteMatrix) -> bytearray:
    """ Converts a 4x4 matrix into a 16-byte vector.  """
    msg: bytearray = bytearray()
    for i in range(0, 4):
        for j in range(0, 4):
            msg.append(matrix[i][j])
            
    return msg
    
    
if __name__ == "__main__":
    matrix: list[list[int]] = [
        [99, 114, 121, 112],
        [116, 111, 123, 105],
        [110, 109, 97, 116],
        [114, 105, 120, 125],
    ]
    
    print(bytes(matrix2array(matrix)))
