"""Tests for AOC 2023-03."""

import pytest

from .advent_2023_03 import gen_gear_ratios, part_numbers, part1, part2


@pytest.fixture(name="schematic")
def _schematic() -> str:
    return """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
    """.strip()


def test_get_minimum_power(schematic: str) -> None:
    """Test minimum_power."""
    assert sorted(part_numbers(schematic)) == sorted(
        [467, 35, 633, 617, 592, 755, 664, 598]
    )


def test_part_1(schematic: str) -> None:
    """Test part1."""
    assert part1(schematic) == 4361


def test_gen_gear_ratios(schematic: str) -> None:
    """Test gen_gear_ratios."""
    assert list(gen_gear_ratios(schematic)) == [16345, 451490]


def test_part_2(schematic: str) -> None:
    """Test part2."""
    assert part2(schematic) == 467835
