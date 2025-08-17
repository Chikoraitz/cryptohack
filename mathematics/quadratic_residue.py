#!/usr/bin/python3
"""
"""

def naive_quadratic_residue_sqrt(x: int, p: int, verbose: bool = False) -> tuple[int, int]:
  """
  """
  sols: list[int] = []
  for i in range(1, p):
    if ((i ** 2) % p) == x:
      sols.append(i)

  if not sols:
    sols += [0, 0]
    if verbose:
      print("No solutions...")
  else:
    if verbose:
      print(f"Solution 1: {sols[0]}, Solution 2: {sols[1]}")

  return tuple(sols)


if __name__ == "__main__":
  p: int = 29
  assert naive_quadratic_residue_sqrt(x=5, p=p) == (11, 18)
  assert naive_quadratic_residue_sqrt(x=18, p=p) == (0, 0)

  ints: list[int] = [14, 6, 11]
  for i in ints:
    sol_1, sol_2 = naive_quadratic_residue_sqrt(x=i, p=p)
    if (sol_1, sol_2) != (0, 0):
      print(f"{i} is a Quadratic Residue with solutions ({sol_1}, {sol_2})")

