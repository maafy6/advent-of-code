"""Solving utilities."""
import asyncio
import inspect
from importlib import import_module
from timeit import timeit
from typing import Any, Awaitable, Callable, List, Optional, Union

import aocd
import pytest


def solve(year: int, day: int, parts: List[int], submit: bool = False) -> int:
    """Run the solution.

    :param year: The year for the challenge.
    :param day: The day for the challenge.
    :param parts: The parts of the challenge to solve.
    :param submit: Submit the answer to the server.
    :returns: A return code.
        1 if there were no solutions, 0 otherwise.
    """
    try:
        module = import_module(f"aoc.aoc_{year}.advent_{year}_{day:02d}")
    except ModuleNotFoundError:
        print(f"No solution for AOC {year}-{day:02d}")
        return 1

    rc = 0
    solutions = {}
    print(f"{year} - {day:02d}\n=========")
    for part in sorted(parts):
        if hasattr(module, f"part{part}"):
            func = getattr(module, f"part{part}")

            def soln_func(
                func: Callable[[], Union[Any, Awaitable[Any]]] = func, part: int = part
            ) -> None:
                if inspect.iscoroutinefunction(func):
                    loop = asyncio.get_event_loop()
                    solution = loop.run_until_complete(func())
                else:
                    solution = func()

                solutions[part] = solution

            soln_time = timeit(soln_func, number=1)
            print(f"Part {part}: {solutions[part]} ({soln_time:.03f} s)")

            if submit:
                part_id = {1: "a", 2: "b"}
                aocd.submit(solutions[part], year=year, day=day, part=part_id[part])
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

    if len(parts) == 1:
        part_markers = " or ".join(f"test_part_{p}" for p in parts)
        markers += f" and ({part_markers})"

    return pytest.main(["-v", "-k", markers])
