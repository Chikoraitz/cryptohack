"""
"""
def quadratic_residue_sqrt(x: int, p: int, p_obeys: str) -> tuple[int, int]:
  """
  """
  if p_obeys == "3 mod 4":
    return __3_mod_4_property(x, p)

  if p_obeys == "1 mod 4":
    return __tonelli_shanks_algorithm(x)

  return -1, -1


def __3_mod_4_property(x: int, p: int) -> tuple[int, int]:
  """
  """
  sol_1: int = pow(x, (p+1) // 4, p)
  sol_2: int = pow(-x, (p+1) // 4, p)
  return sol_1, sol_2


def __tonelli_shanks_algorithm(x: int) -> tuple[int, int]:
  """
  """
  return -1, -1


