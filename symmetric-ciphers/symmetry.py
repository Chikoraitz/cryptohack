#!/usr/bin/python3

import requests

from simplejson.errors import JSONDecodeError


CRYPTOHACK_CHALLENGE_ENDPOINT: str = "http://aes.cryptohack.org/symmetry"


def __encrypt(plaintext: str, iv: str) -> str:
  """Challenge endpoint that returns AES-encrypted ciphertext in OFB mode
  """
  resp = requests.get(f"{CRYPTOHACK_CHALLENGE_ENDPOINT}/encrypt/{plaintext}/{iv}/")
  try:
    if "error" in resp.json():
      raise Exception(resp.json()["error"])

    return resp.json()["ciphertext"]
  except JSONDecodeError:
    print("Malformed hex input in __encrypt()")


def __encrypt_flag() -> str:
  """Challenge endpoint that returns the flag plaintext DES-encrypted in ECB mode
  """
  resp = requests.get(f"{CRYPTOHACK_CHALLENGE_ENDPOINT}/encrypt_flag/")
  return resp.json()["ciphertext"]


def challenge_solution(verbose: bool = True) -> str:
  """OFB mode is XOR symmetric, meaning that encryption and decryption are exactly the same
  """
  ciphertext: str = __encrypt_flag()
  iv: str = ciphertext[:32]
  plaintext_hex: str = __encrypt(ciphertext[32:], iv)

  if verbose:
    print(f"IV: {iv}")

  return bytes.fromhex(plaintext_hex).decode("utf-8" )


if __name__ == "__main__":
  flag: str = challenge_solution(verbose=False)
  print(f"Flag: {flag}")
