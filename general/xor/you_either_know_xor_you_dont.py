import sys

byte_data = bytes.fromhex(sys.argv[1])
known_substring = b'crypto{'
key = []

def break_xor(key_size):
    hex_msg = []
    for index, byte in enumerate(byte_data):
        hex_msg.append(hex(key[index % key_size] ^ byte)[2:].zfill(2))
    
    msg = bytes.fromhex(''.join(hex_msg))
    print(f"Key: {[chr(i) for i in key]}, Flag: {msg}")

# The flag prefix is 7 characters long, so the key gets truncated at 'myXORke'
for key_size in range(1,len(known_substring) + 1):
    for i in range(256):
        flag_prefix_i = i ^ byte_data[key_size - 1]
        if chr(known_substring[key_size - 1]) == chr(flag_prefix_i):
            key.append(i)
            break
        
    break_xor(key_size)
    
# Last character of the key is 'y'
key.append(ord('y'))
key_size = len(known_substring) + 1
break_xor(key_size)