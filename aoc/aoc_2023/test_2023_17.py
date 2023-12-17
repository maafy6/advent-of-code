"""Tests for AOC 2023-17."""

from textwrap import dedent

import pytest

from .advent_2023_17 import a_star, parse_input


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        """
            2413432311323
            3215453535623
            3255245654254
            3446585845452
            4546657867536
            1438598798454
            4457876987766
            3637877979653
            4654967986887
            4564679986453
            1224686865563
            2546548887735
            4322674655533
        """
    ).strip()


@pytest.mark.parametrize(
    ("data", "min_dist", "max_dist", "expected"),
    [
        (
            dedent(
                """
                    2413432311323
                    3215453535623
                    3255245654254
                    3446585845452
                    4546657867536
                    1438598798454
                    4457876987766
                    3637877979653
                    4654967986887
                    4564679986453
                    1224686865563
                    2546548887735
                    4322674655533
                """
            ).strip(),
            1,
            3,
            102,
        ),
        (
            dedent(
                """
                    2413432311323
                    3215453535623
                    3255245654254
                    3446585845452
                    4546657867536
                    1438598798454
                    4457876987766
                    3637877979653
                    4654967986887
                    4564679986453
                    1224686865563
                    2546548887735
                    4322674655533
                """
            ).strip(),
            4,
            10,
            94,
        ),
        (
            dedent(
                """
                    111111111111
                    999999999991
                    999999999991
                    999999999991
                    999999999991
                """
            ).strip(),
            4,
            10,
            71,
        ),
    ],
)
def test_a_star(data: str, min_dist: int, max_dist: int, expected: int) -> None:
    """Test a_star."""
    grid = parse_input(data)
    assert a_star(grid, min_dist, max_dist) == expected
