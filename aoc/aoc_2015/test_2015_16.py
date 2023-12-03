"""Tests for AOC 2015-16."""

from .advent_2015_16 import Sue


def test_sue() -> None:
    """Test Sue.from_desc."""
    sue = Sue.from_desc("Sue 1: goldfish: 9, cars: 0, samoyeds: 9")
    assert sue == Sue(id=1, goldfish=9, cars=0, samoyeds=9)
    assert sue.children is None
