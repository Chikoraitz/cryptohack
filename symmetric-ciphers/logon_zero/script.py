#!/usr/bin/python3

import json
import pwn as pwntools
import re
import time


#r = pwntools.remote("localhost", 13399)
r = pwntools.remote("socket.cryptohack.org", 13399)


def __send_to_connection(verbose: bool, option: str, _input: dict[str, str] = {}) -> str:
  """Facilitates the interaction with the server
  """
  payload: dict[str, str] = {"option": option}
  payload.update(_input)
  payload_str: str = json.dumps(payload).encode()
  if verbose:
    print(f"[+] Sending: {payload_str}")
  r.send(payload_str)

  data: bytes = r.recvline()
  data_json = json.loads(data.decode("utf-8"))

  if "exception" in data_json.keys():
    raise Exception(data_json["exception"])

  if "msg" in data_json.keys():
    return data_json["msg"]


def logonzero_exploit(verbose = True) -> str:
  """Solution to the LogonZero encryption challenge
  """
  flag: str = ""
  payload_input: bytes = b'\x00' * 30

  try:
    # Brute-force
    for i in range(255):
      resp: str = __send_to_connection(verbose, "reset_password", {"token": payload_input.hex()})
      if verbose:
        print(f"  [-] {resp}")
      resp = __send_to_connection(verbose, "authenticate", {"password": ""})
      if verbose:
        print(f"  [-] {resp}")
      if "Welcome admin" in resp:
        flag = re.search('.*(crypto{.+}).*', resp).group(1)
        break
      else:
        resp = __send_to_connection(verbose, "reset_connection")
        if verbose:
          print(f"  [-] {resp}")

      time.sleep(1)
  except Exception:
    r.shutdown()
    r.wait_for_close()

  return flag

if __name__ == "__main__":
  r.recvuntil(b'Please authenticate to this Domain Controller to proceed\n')
  flag: str = logonzero_exploit()
  print(f"Flag: {flag}")
