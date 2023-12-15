"""Tests for AOC 2023-15."""

import pytest

from .advent_2023_15 import holiday_hash, initialization_sequence, part1, part2


@pytest.fixture(name="data")
def _data() -> str:
    return """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("HASH", 52),
        ("rn=1", 30),
        ("cm-", 253),
        ("qp=3", 97),
        ("cm=2", 47),
        ("qp-", 14),
        ("pc=4", 180),
        ("ot=9", 9),
        ("ab=5", 197),
        ("pc-", 48),
        ("pc=6", 214),
        ("ot=7", 231),
    ],
)
def test_holiday_hash(s: str, expected: int) -> None:
    """Test holiday_hash."""
    assert holiday_hash(s) == expected


def test_initialization_sequence(data: str) -> None:
    """Test initialization sequence."""
    assert initialization_sequence(data.split(",")) == {
        0: {"rn": 1, "cm": 2},
        1: {},
        3: {"ot": 7, "ab": 5, "pc": 6},
    }


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 1320


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 145
