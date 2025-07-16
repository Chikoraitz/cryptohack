#!/usr/bin/python3

import requests

from PIL import Image
from simplejson.errors import JSONDecodeError
from typing import IO


CRYPTOHACK_CHALLENGE_ENDPOINT: str = "http://aes.cryptohack.org/bean_counter/encrypt/"
AES_BLOCK_SIZE: int = 16
AES_BLOCK_HEX_SIZE: int = AES_BLOCK_SIZE * 2


def __get_encrypted_img() -> str:
  """Challenge endpoint that returns an AES-encrypted ciphertext of an image in CTR mode
  """
  resp = requests.get(f"{CRYPTOHACK_CHALLENGE_ENDPOINT}")
  try:
     return resp.json()["encrypted"]
  except JSONDecodeError:
    print("JSON decoding error in __encrypt()")


def __open_img(img_bin: bytes, verbose: bool) -> None:
  """From a binary image, open and show the image
  """
  from io import BytesIO

  img_bin_io: IO[bytes] = BytesIO(img_bin)
  img = Image.open(img_bin_io)
  img.show()


def decrypt_img(verbose: bool = True) -> None:
  """Due to an implementation error, the counter is not updated.
  """
  png_file_signature: bytes = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'
  png_ihdr: bytes = b'\x00\x00\x00\x0d\x49\x48\x44\x52'
  png_header: bytes = png_file_signature + png_ihdr

  encrypted_img: bytes = bytes.fromhex(__get_encrypted_img())

  if verbose:
    print(f"PNG Header: {png_header}")
    print(f"Encrypted image: {encrypted_img[:AES_BLOCK_HEX_SIZE]} ... {encrypted_img[-15:-1]}")

  block_cipher: bytearray = [png_header[i] ^ cipher for i, cipher in enumerate(encrypted_img[:AES_BLOCK_SIZE])]
  decrypted_img: bytearray = [block_cipher[i % AES_BLOCK_SIZE] ^ cipher for i, cipher in enumerate(encrypted_img)]
  __open_img(bytes(decrypted_img), verbose)


if __name__ == "__main__":
  decrypt_img(verbose=False)

