"""Tests for AOC 2015-10."""

import pytest

from .advent_2015_10 import elf_say


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("1", "11"),
        ("11", "21"),
        ("21", "1211"),
        ("1211", "111221"),
        ("111221", "312211"),
    ],
)
def test_elf_say(value: str, expected: str) -> None:
    """Test elf_say."""
    assert elf_say(value) == expected
