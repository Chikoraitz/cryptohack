import sys

KEY1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
KEY2_KEY1 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
KEY2_KEY3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
FLAG_KEY1_KEY2_KEY3 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

def xor(arg1: str, arg2: str)->str:
    """XOR operation over two hex strings
    """
    ARG1 = bytes.fromhex(arg1)
    ARG2 = bytes.fromhex(arg2)
    xor = [hex(ARG1[i] ^ ele)[2:].zfill(2) for i,ele in enumerate(ARG2)]
    return ''.join(xor)
    
print(f"Key 1: {KEY1}")

KEY2 = xor(KEY1, KEY2_KEY1)
print(f"Key 2: {KEY2}")

KEY3 = xor(KEY2, KEY2_KEY3)
print(f"Key 3: {KEY3}")

KEY123 = xor(KEY1, KEY2_KEY3)
FLAG = xor(KEY123, FLAG_KEY1_KEY2_KEY3)
print(f"Flag: {bytes.fromhex(FLAG)}")