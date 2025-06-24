import sys
import base64

flag = base64.b64encode(bytes.fromhex(sys.argv[1]))
print(f"{flag}")