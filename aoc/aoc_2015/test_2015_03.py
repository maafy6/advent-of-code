"""Tests for AOC 2015-03."""

import pytest

from .advent_2015_03 import part1, part2


@pytest.mark.parametrize(
    ("instructions", "houses"),
    [
        (">", 2),
        ("^>v<", 4),
        ("^v^v^v^v^v", 2),
    ],
)
def test_part_1(instructions: str, houses: int) -> None:
    """Test part 1."""
    assert part1(instructions) == houses


@pytest.mark.parametrize(
    ("instructions", "houses"),
    [
        ("^v", 3),
        ("^>v<", 3),
        ("^v^v^v^v^v", 11),
    ],
)
def test_part_2(instructions: str, houses: int) -> None:
    """Test part 2."""
    assert part2(instructions) == houses
