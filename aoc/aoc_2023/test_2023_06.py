"""Tests for AOC 2023-06."""

from textwrap import dedent

import pytest

from .advent_2023_06 import part1, part2, race_outcomes


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        """
        Time:      7  15   30
        Distance:  9  40  200
        """
    ).strip()


def test_race_outcomes() -> None:
    """Test race_outcomes."""
    assert race_outcomes(7, 9) == 4


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 288


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 71503
