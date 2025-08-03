#!/usr/bin/python3

import requests
import string

from simplejson.errors import JSONDecodeError


CRYPTOHACK_CHALLENGE_ENDPOINT: str = "http://aes.cryptohack.org/ctrime/encrypt"


def __encrypt(plaintext: str) -> str:
  """Challenge endpoint that returns AES-encrypted ciphertext in CTR mode
  """
  resp = requests.get(f"{CRYPTOHACK_CHALLENGE_ENDPOINT}/{plaintext}/")
  try:
    if "error" in resp.json():
      raise Exception(resp.json()["error"])

    return resp.json()["ciphertext"]
  except JSONDecodeError:
    print("Malformed hex input in __encrypt()")


def crime_exploit(verbose: bool = True) -> str:
  """
  Before encryption, the plaintext is concatenated to the flag and zlib-compressed.
  This setup is vulnerable to known password attacks - we already know that the flag
  has the prefix 'crypto{'.
  """
  flag: str = "crypto{"
  hit_char: str = ''

  while hit_char != '}':
    wrong_guess: str = flag + '*'
    # For some reason related to the DEFLATE algorithm that I couldn't figure out
    # the brute-force process breaks at 'crypto{CRIM' if the input is a single guess.
    # Hence, to improve the repeatability and robustness of the exploit, it is better
    # to (at least) duplicate the plaintext input payload.
    ref_cipher_len: int = len(__encrypt((wrong_guess * 2).encode().hex()))

    if verbose:
      print(f"[+] Guess iteration: {wrong_guess}, ", end='')

    for c in string.printable:
      payload: str = flag + c
      # Payload duplication
      test_cipher_len: int = len(__encrypt((payload * 2).encode().hex()))

      if test_cipher_len < ref_cipher_len:
        hit_char = c
        flag += hit_char
        if verbose:
          print(f"HIT: {hit_char}")
        break

    if flag != payload:
      raise Exception("End of character space without HIT...")

  return flag


if __name__ == "__main__":
  flag: str = crime_exploit()
  print(f"Flag: {flag}")
