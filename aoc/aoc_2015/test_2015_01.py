"""Tests for AOC 2015-01."""

import pytest

from .advent_2015_01 import part1, part2


@pytest.mark.parametrize(
    ("instructions", "floor"),
    [
        ("(())", 0),
        ("()()", 0),
        ("(((", 3),
        ("(()(()(", 3),
        ("))(((((", 3),
        ("())", -1),
        ("))(", -1),
        (")))", -3),
        (")())())", -3),
    ],
)
def test_part_1(instructions: str, floor: int) -> None:
    """Test part 1."""
    assert part1(instructions) == floor


@pytest.mark.parametrize(
    ("instructions", "floor"),
    [
        (")", 1),
        ("()())", 5),
    ],
)
def test_part_2(instructions: str, floor: int) -> None:
    """Test part 2."""
    assert part2(instructions) == floor
