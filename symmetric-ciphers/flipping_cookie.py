#!/usr/bin/python3
import requests
import traceback


def __get_cookie(verbose: bool = True) -> str:
  """Get encrypted content of the cookie"""
  resp = requests.get("http://aes.cryptohack.org/flipping_cookie/get_cookie/")
  cookie: str = resp.json()["cookie"]

  if verbose:
    print(f"Cookie: {cookie}")

  return cookie


def __new_iv(iv: bytes, msg: str, tampered_msg: str, verbose: bool = True) -> bytes:
  """Leverage the associative property of XOR operation to calculate how the IV
  should be change for the XOR operation to return 'tampered_msg' instead of 'msg'.
  This function assumes that the 16-byte block starts with 'msg', i.e., no prefix.
  'msg' and 'tampered_msg' should be the same size.
  """
  if len(msg) != len(tampered_msg):
    raise Exception("'msg' and 'tampered_msg' are not the same size")

  msg_bytearray: bytearray = [byte for byte in msg.encode()]
  tampered_msg_bytearray: bytearray = [byte for byte in tampered_msg.encode()]
  iv_bytearray: bytearray = [byte for byte in iv]
  diff: bytearray = [0x0 for _ in range(len(iv))]

  for i in range(len(msg)):
    diff[i] = msg_bytearray[i] ^ tampered_msg_bytearray[i]

  new_iv: bytearray = [diff[i] ^ value for i, value in enumerate(iv_bytearray)]

  if verbose:
    print(f"Original IV: {iv.hex()}, New IV: {bytes(new_iv).hex()}")

  return bytes(new_iv)


def bit_flipping_attack(cookie: str, verbose: bool = True) -> str:
  """The cookie implementation is vulnerable to data integrity attacks
  The cookie payload has the following prefix:
  - expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
  - 'admin=False;expiry={expire_at}'
  The cookie ciphertext = IV + encrypted_msg
  """
  original_iv: bytes = bytes.fromhex(cookie[:32])
  tampered_iv: bytes = __new_iv(original_iv, "admin=False", ";admin=True", verbose) # Match the number of characters
  tampered_cookie: str = tampered_iv.hex() + cookie[32:]

  if verbose:
    print(f"URL: http://aes.cryptohack.org/flipping_cookie/check_admin/{tampered_cookie}/{tampered_iv.hex()}/")

  check_admin_resp = requests.get(f"http://aes.cryptohack.org/flipping_cookie/check_admin/{tampered_cookie}/{tampered_iv.hex()}/")

  try:
    resp = check_admin_resp.json()
    return resp["flag"]
  except KeyError:
    return resp["error"]
  except:
    traceback.print_exc()
    return ""

if __name__ == "__main__":
  cookie: str = __get_cookie(verbose=False)
  flag = bit_flipping_attack(cookie, verbose=False)
  print(f"Flag: {flag}")
