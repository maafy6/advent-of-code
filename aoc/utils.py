"""Generic utilities for Advent of Code."""

import itertools
import math
from typing import Iterable, Iterator, Mapping


def euclid_sequence(m: int, n: int) -> Iterator[tuple[int, int]]:
    """Yield the sequence of remainders and quotients from Euclid's algorithm.

    :param m: The first number.
    :param n: The second number.
    :yields: Sequential tuples `r,q` representing the remainder and quotient
        from Euclid's algorith at each step of the algorithm.
    """
    s2, s1 = (max(m, n), 0), (min(m, n), 0)
    while s1[0] != 0:
        rq = (s2[0] % s1[0], s2[0] // s1[0])
        yield rq
        s2, s1 = s1, rq


def bezout_coefficients(m: int, n: int) -> tuple[int, int]:
    """Calculate the Bézout coefficients for m and n.

    The Bézout coefficients `u`, `v` satisfy the condition
    `u*m + v*n = gcd(m, n)`

    :param m: The first number.
    :param n: The second number.
    :returns: A tuple `u,v` that satisifies the Bézout equation.
    """
    m, n = max(m, n), min(m, n)

    a, b, c, d = 1, 0, 0, 1
    for _, q in euclid_sequence(m, n):
        a, b = a * q + b, a
        c, d = c * q + d, c

    return d, -b


def chinese_remainder_theorem(
    mod_values: Mapping[str, Iterable[int]], moduli: Mapping[str, int]
) -> tuple[list[int], int]:
    """Apply Chinese remainder theorem to a system of mods.

    :param mod_values: A mapping of a group ID to a sequence of possible
        solutions.
    :param moduli: A mapping of group ID to the modulus for that group.
    :returns: A tuple of a list of possible solutions and the solution modulus.
    """
    loop_ids = list(mod_values.keys())
    solutions, modulo = None, None
    while loop_ids:
        loop_id = loop_ids.pop()
        z_mods = mod_values[loop_id]
        loop_mod = moduli[loop_id]

        if solutions is None:
            solutions = z_mods
            modulo = loop_mod
            continue

        solns = []
        for s, z in itertools.product(solutions, z_mods):
            _, v = bezout_coefficients(modulo, loop_mod)
            l = (s - z) // math.gcd(modulo, loop_mod)
            solns.append(z + loop_mod * l * v)

        modulo = math.lcm(modulo, loop_mod)
        solutions = [s % modulo for s in solns]

    return solutions, modulo
