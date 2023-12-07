"""Tests for AOC 2023-07."""

from textwrap import dedent

import pytest

from .advent_2023_07 import part1, part2


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        """
    ).strip()


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 6440


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 5905
