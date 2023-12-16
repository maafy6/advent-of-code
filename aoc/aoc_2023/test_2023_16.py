"""Tests for AOC 2023-16."""

from textwrap import dedent

import pytest

from .advent_2023_16 import part1, part2


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        r"""
            .|...\....
            |.-.\.....
            .....|-...
            ........|.
            ..........
            .........\
            ..../.\\..
            .-.-/..|..
            .|....-|.\
            ..//.|....
        """
    ).strip()


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 46


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 51
