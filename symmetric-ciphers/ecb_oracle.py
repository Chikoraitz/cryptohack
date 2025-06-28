#!/usr/bin/python3

import os
import requests
import string
import time


def __get_ciphertext_resp(plaintext: str) -> str:
  """Challenge endpoint that returns ECB ciphertext"""
  resp = requests.get(f"http://aes.cryptohack.org/ecb_oracle/encrypt/{plaintext}/")

  return resp.json()["ciphertext"]


def __aes_blocks(n: int) -> int:
  """Return number of bytes in n AES blocks"""
  return 16 * n


def ecb_padding_attack(verbose: bool = True) -> str:
  """AES in ECB mode is vulnerable to guess plaintext/ciphertext without knowning
  the key by using padding
  The encryption endpoint appends the plantext to the flag: enc(plaintext + flag)
  """
  flag: str = "crypto{"
  guess_char: str = ""
  char_space: str = '_'+'@'+'}'+string.digits + string.ascii_lowercase + string.ascii_uppercase
  guess_char: str = ''

  while guess_char != '}':
    payload: str = (('1') * (__aes_blocks(2) - len(flag) - 1))
    expected_ciphertext: str = __get_ciphertext_resp(payload.encode().hex())

    for c in char_space:
      if verbose:
        print(f"Flag: {flag}, Expected ciphertext:\n {expected_ciphertext[:32]}\n {expected_ciphertext[32:64]}\n {expected_ciphertext[64:96]}\n {expected_ciphertext[96:128]}")
        print(f"\nGuess: {c}, Payload: ", end='')

      payload_test: str = payload + flag +c
      test_ciphertext: str = __get_ciphertext_resp(payload_test.encode().hex())

      if verbose:
        print(f"{payload_test}")
        print(f"Test ciphertext:\n {test_ciphertext[:32]}\n {test_ciphertext[32:64]}\n {test_ciphertext[64:96]}\n {test_ciphertext[96:128]}")

      if test_ciphertext[32:64] == expected_ciphertext[32:64]:
        guess_char = c
        flag += c
        print(flag)
        break

      time.sleep(0.5)

      if verbose:
        if os.name == 'nt':
          _ = os.system('cls')
        else:
          _ = os.system('clear')

  return flag


if __name__ == "__main__":
  flag: str = ecb_padding_attack(verbose=False)
  print(flag)
