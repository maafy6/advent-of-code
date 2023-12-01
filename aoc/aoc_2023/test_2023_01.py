"""Tests for AOC 2023-01."""

from .advent_2023_01 import part1, part2


def test_part_1() -> None:
    """Test part 1."""
    data = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
    """.strip()

    assert part1(data) == 142


def test_part_2() -> None:
    """Test part 2."""
    data = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
    """.strip()

    assert part2(data) == 281
