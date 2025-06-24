import sys

data = bytes.fromhex(sys.argv[1])
for i in range(256):
    hex_msg = [hex(i ^ byte)[2:].zfill(2) for byte in data]
    msg = bytes.fromhex(''.join(hex_msg))
    if b'crypto{' in msg:
        print(f"Favourite byte: {hex(i)}, Flag: {msg}")
        break