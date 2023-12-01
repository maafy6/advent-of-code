"""Solving utilities."""
from typing import List, Optional
from importlib import import_module

import pytest


def solve(year: int, day: int, parts: List[int]) -> int:
    """Run the solution.

    :param year: The year for the challenge.
    :param day: The day for the challenge.
    :param parts: The parts of the challenge to solve.
    :returns: A return code.
        1 if there were no solutions, 0 otherwise.
    """
    try:
        module = import_module(f"aoc.aoc_{year}.advent_{year}_{day:02d}")
    except ModuleNotFoundError:
        print(f"No solution for AOC {year}-{day:02d}")
        return 1

    rc = 0
    for part in sorted(parts):
        if hasattr(module, f"part{part}"):
            func = getattr(module, f"part{part}")
            solution = func()
            print(f"Part {part}: {solution}")
        else:
            print(f"No solution for AOC {year}-{day:02d} Part {part}")
            rc = 1

    return rc


def test(year: int, day: int, parts: Optional[List[int]] = None) -> int:
    """Run the tests.

    :param year: The year for the challenge.
    :param day: The day for the challenge.
    :param parts: The parts of the challenge to test.
    :returns: The pytest return code.
    """
    markers = f"test_{year}_{day:02d}"

    if parts:
        part_markers = " or ".join(f"test_part_{p}" for p in parts)
        markers += f" and ({part_markers})"

    return pytest.main(["-v", "-k", markers])
