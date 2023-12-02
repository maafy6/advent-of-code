"""Tests for AOC 2015-04."""

import pytest

from .advent_2015_04 import part1  # , part2


@pytest.mark.parametrize(
    ("secret", "answer"),
    [
        ("abcdef", 609043),
        ("pqrstuv", 1048970),
    ],
)
def test_part_1(secret: str, answer: int) -> None:
    """Test part 1."""
    assert part1(secret) == answer
