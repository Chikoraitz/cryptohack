#!/usr/bin/python3

import requests

from simplejson.errors import JSONDecodeError


CRYPTOHACK_CHALLENGE_ENDPOINT: str = "http://aes.cryptohack.org/triple_des"


def __encrypt(key: str, plaintext: str) -> str:
  """Challenge endpoint that returns DES-encrypted ciphertext in ECB mode
  """
  resp = requests.get(f"{CRYPTOHACK_CHALLENGE_ENDPOINT}/encrypt/{key}/{plaintext}/")
  try:
    if "error" in resp.json():
      raise Exception(resp.json()["error"])

    return resp.json()["ciphertext"]
  except JSONDecodeError:
    print("Malformed hex input in __encrypt()")


def __encrypt_flag(key: str) -> str:
  """Challenge endpoint that returns the flag plaintext DES-encrypted in ECB mode
  """
  resp = requests.get(f"{CRYPTOHACK_CHALLENGE_ENDPOINT}/encrypt_flag/{key}/")
  try:
    if "error" in resp.json():
      raise Exception(resp.json()["error"])

    return resp.json()["ciphertext"]
  except JSONDecodeError:
    print("Malformed hex input in __encrypt()")


def weak_key_exploit(verbose: bool = True) -> str:
  """Access to the encryption process and being the key user-controllable, this
  system is vulnerable to a weak key. In 3DES, weak keys reduce the encryption
  to a single DES operation.
  """
  # The key must be 16 or 24 bytes long and should bypass the PyCryptodome library
  # weak key checks
  weak_key: bytes = b'\x00' * 8 + b'\xff' * 8
  if verbose:
    print(f"Weak key: {weak_key.hex()}")

  flag_cipher: str = __encrypt_flag(weak_key.hex())
  if verbose:
    print(f"Flag cipher: {flag_cipher}")

  decrypt_resp: str = __encrypt(weak_key.hex(), flag_cipher)
  plaintext: str = bytes.fromhex(decrypt_resp).decode("utf-8")

  return plaintext


if __name__ == "__main__":
  flag: str = weak_key_exploit(verbose=False)
  print(f"Flag: {flag}")
