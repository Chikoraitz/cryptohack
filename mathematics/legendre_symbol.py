#!/usr/bin/python3

from pathlib import Path

from modular_math import quadratic_residue_sqrt


def is_quadratic_residue(a: int, p: int, verbose: bool = False) -> bool:
  """Applies the Legendre Symbol to check is "a" is a quadratic residue.
  """
  try:
    if a == 0 or (a % p) == 0:
      raise ValueError

    a_div_p: int = pow(a, (p-1) // 2, p)
    if verbose:
      print(f"(a/p) = {a_div_p}")

    if a_div_p == 1:
      return True

    # a_div_p == p - 1
    return False

  except ValueError:
    print(f"Error: p is not prime; a = 0 (mod p), so (a/p) = 0...")
    return False


if __name__ == "__main__":
  assert is_quadratic_residue(a=14, p=29) == False
  assert is_quadratic_residue(a=6, p=29) == True
  assert is_quadratic_residue(a=11, p=29) == False

  file_vars: dict[str, int] = {}

  exec(open(Path(__file__).parent / "output/legendre_symbol.txt").read(), globals(), file_vars)
  p: int = file_vars["p"]
  ints: list[int] = file_vars["ints"]
  for x in ints:
    if is_quadratic_residue(x, p, verbose=False):
      print(f"{x} is a Quadratic Residue")
      root_1, root_2 = quadratic_residue_sqrt(x, p, p_obeys="3 mod 4")
      print(f"The larger of the two is: {max(root_1, root_2)}")
