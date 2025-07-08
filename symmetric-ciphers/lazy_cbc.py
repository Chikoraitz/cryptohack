#!/usr/bin/python3

import os
import requests

from simplejson.errors import JSONDecodeError


CRYPTOHACK_CHALLENGE_ENDPOINT: str = "http://aes.cryptohack.org/lazy_cbc"
AES_BLOCK_SIZE: int = 16 # bytes
HEX_AES_BLOCK_SIZE: int = AES_BLOCK_SIZE * 2


def __encrypt(plaintext: str) -> str:
  """Challenge endpoint that returns a lazy AES in CBC mode from a
  user-controllable plaintext
  """
  resp = requests.get(f"{CRYPTOHACK_CHALLENGE_ENDPOINT}/encrypt/{plaintext}/")

  try:
    if "error" in resp.json():
      raise Exception(resp.json()["error"])

    return resp.json()["ciphertext"]

  except JSONDecodeError:
    print("Malformed hex input in __encrypt()")

def __receive(ciphertext: str) -> dict[str, str]:
  """Challenge endpoint that returns the decrypted plaintext from a provided ciphertext
  """
  resp = requests.get(f"{CRYPTOHACK_CHALLENGE_ENDPOINT}/receive/{ciphertext}/")

  try:
    if "error" in resp.json() and ("Invalid plaintext" not in resp.json()["error"]):
      raise Exception(resp.json()["error"])

    return resp.json()

  except JSONDecodeError:
    print("Malformed hex input in __receive()")


def __get_flag(key: str) -> str:
  """Challenge endpoint that returns the flag if the input matches the AES key
  """
  resp = requests.get(f"{CRYPTOHACK_CHALLENGE_ENDPOINT}/get_flag/{key}/")

  try:
    if "error" in resp.json():
      raise Exception(resp.json()["error"])

    return resp.json()["plaintext"]

  except JSONDecodeError:
    print("Malformed hex input in __get_flag()")


def exploit(verbose: bool = True) -> str:
  """The challenge encryption is flawed.
  The implementation does not use a cryptographic secure random generator to generate the IV.
  Instead it reutilizes the key as IV.
  """
  plaintext_bytes: bytes = os.urandom(AES_BLOCK_SIZE * 3)
  plaintext_hex: str = plaintext_bytes.hex()

  if verbose:
    print(f"Original plaintext: {plaintext_hex}")

  ciphertext: str = __encrypt(plaintext_hex)
  tampered_ciphertext: str = ciphertext[:HEX_AES_BLOCK_SIZE] +\
                              ("0" * HEX_AES_BLOCK_SIZE) +\
                              ciphertext[:HEX_AES_BLOCK_SIZE]

  if verbose:
    print(f"Original ciphertext: {ciphertext}")
    print(f"Tampered ciphertext: {tampered_ciphertext}")

  status: dict[str, str] = __receive(tampered_ciphertext)
  prefix: str = "Invalid plaintext: "


  if ("error" in status) and (prefix in status["error"]):
    tampered_plaintext: str = status["error"].replace(prefix, '')
    tampered_plaintext_bytes: bytes = bytes.fromhex(tampered_plaintext)
    key_bytes: bytearray = [tampered_plaintext_bytes[i] ^ tampered_plaintext_bytes[i + (AES_BLOCK_SIZE*2)]\
    for i in range(AES_BLOCK_SIZE)]

    if verbose:
      print(f"Tampered plaintext: {tampered_plaintext}")
      print(f"AES Key: {bytes(key_bytes).hex()}")

    flag_hex: str = __get_flag(bytes(key_bytes).hex())

    if verbose:
      print(f"Flag bytes: {flag_hex}")

    return bytes.fromhex(flag_hex).decode()

  else:
    print(f"Received a success response: {status['success']}")
    return bytes(0)


if __name__ == "__main__":
  flag: str = exploit(verbose=False)
  print(f"Flag: {flag}")
