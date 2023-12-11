"""Tests for AOC 2023-11."""

from textwrap import dedent

import pytest

from .advent_2023_11 import get_distance_sum, parse_input


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        """\
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        """
    ).strip()


@pytest.mark.parametrize(
    ("age", "expected"), [(1, 374), (10 - 1, 1030), (100 - 1, 8410)]
)
def test_get_distance_sum(age: int, expected: int, data: str) -> None:
    """Test get_distance_sum."""
    universe = parse_input(data)
    assert get_distance_sum(universe, age) == expected
