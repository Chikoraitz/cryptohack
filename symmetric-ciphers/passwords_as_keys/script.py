#!/usr/bin/python3

import sys
import hashlib

from Crypto.Cipher import AES


def bruteforce(cipher: str) -> str:
  """Key Brute-force

  The key was derived randomly from a well-known list of words
  """
  with open("words.txt", 'r') as f:
    words = [w.strip() for w in f.readlines()]

  for word in words:
    key_test: bytes = hashlib.md5(word.encode()).digest()
    result: str = __decrypt(cipher, key_test)

    if result != "Failed":
      print(f"Word: {word}, Hash: {key_test.hex()}")
      return result

  return ""


def __decrypt(ciphertext: str, pwd_hash: bytes) -> str:
  """Decrypt AES ciphertext"""
  cipher_bytes: bytes = bytes.fromhex(ciphertext)
  aes_cipher = AES.new(pwd_hash, AES.MODE_ECB)

  try:
    decrypted: str = aes_cipher.decrypt(cipher_bytes).decode()
  except ValueError as e:
    return "Failed"
  else:
    if "crypto{" in decrypted:
       return  decrypted
    return "Failed"


if __name__ == "__main__":
  assert len(sys.argv) == 2, "This script requires one argument: ciphertext"
  flag: str = bruteforce(sys.argv[1])

  print(f"Flag: {flag}")
