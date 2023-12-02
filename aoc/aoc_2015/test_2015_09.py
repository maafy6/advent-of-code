"""Tests for AOC 2015-09."""

import pytest

from .advent_2015_09 import part1, part2


@pytest.fixture(name="distances")
def _distances() -> str:
    return """
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
    """.strip()


def test_part_1(distances: str) -> None:
    """Test part 1."""
    assert part1(distances) == 605


def test_part_2(distances: str) -> None:
    """Test part 2."""
    assert part2(distances) == 982
