"""Tests for AOC 2015-02."""

import pytest

from .advent_2015_02 import part1, part2


@pytest.mark.parametrize(
    ("dimensions", "area"),
    [
        ("2x3x4", 58),
        ("1x1x10", 43),
    ],
)
def test_part_1(dimensions: str, area: int) -> None:
    """Test part 1."""
    assert part1(dimensions) == area


@pytest.mark.parametrize(
    ("dimensions", "length"),
    [
        ("2x3x4", 34),
        ("1x1x10", 14),
    ],
)
def test_part_2(dimensions: str, length: int) -> None:
    """Test part 2."""
    assert part2(dimensions) == length
