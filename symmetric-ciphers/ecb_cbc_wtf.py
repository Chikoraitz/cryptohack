#!/usr/bin/python3
import sys
import requests


def get_challenge_parameters() -> tuple[str, str]:
  """Solution automation by retrieving the ciphertext and plaintext directly from
  the provided web endpoints
  """
  encrypt_resp = requests.get("http://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/")
  ciphertext: str = encrypt_resp.json()["ciphertext"]
  ecb_decrypt_resp = requests.get(f"http://aes.cryptohack.org/ecbcbcwtf/decrypt/{ciphertext}/")
  ecb_plaintext: str = ecb_decrypt_resp.json()["plaintext"]

  return ciphertext, ecb_plaintext 


def get_cbc_plaintext(ciphertext: str, ecb_plaintext: str) -> str:
  """The ciphertext encrypted in CBC and plaintext decrypted in ECB are provided.
  The IV is generated randomly at each request.

  Returns the plaintext encrypted in CBC mode
  - The IV is the first 16 bytes of the ciphertext (iv + encrypted)
  - The first block of the ciphertext is (encrypted = AES(iv XOR p0, key))
  - The remaining blocks are derived from the previous
  """
  cipherbytes: bytearray = bytearray.fromhex(ciphertext)
  ecb_plainbytes: bytearray = bytearray.fromhex(ecb_plaintext)
  cipher_blocks: int = int((len(cipherbytes) / 16))

  # Block 0
  # iv: bytearray = cipherbytes[:16]
  # cbc_plaintext: str = bytes(a ^ b for a,b in zip(ecb_plainbytes[16:32], iv)).decode()

  cbc_plaintext: str = ""

  # Iterate over cipher blocks
  for n_block in range(1, cipher_blocks):
    cbc_plaintext += bytes(a ^ b for a,b in zip(ecb_plainbytes[(n_block * 16):((n_block + 1) * 16)],
    cipherbytes[((n_block - 1)*16):(n_block * 16)])).decode()

  return cbc_plaintext


if __name__ == "__main__":
  ciphertext, ecb_plaintext = get_challenge_parameters()
  flag: str = get_cbc_plaintext(ciphertext, ecb_plaintext)

  print(f"Flag: {flag}")
