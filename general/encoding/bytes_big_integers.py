import sys
from Crypto.Util.number import long_to_bytes

dec_number = int(sys.argv[1], 10)
print(type(dec_number))
print(f"{long_to_bytes(dec_number)}")
