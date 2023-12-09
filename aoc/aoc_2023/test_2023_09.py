"""Tests for AOC 2023-09."""

from textwrap import dedent

import pytest

from .advent_2023_09 import part1, part2, predict


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        """
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
    """
    ).strip()


@pytest.mark.parametrize(
    ("report", "expected"),
    [
        ("0 3 6 9 12 15", 18),
        ("1 3 6 10 15 21", 28),
        ("10 13 16 21 30 45", 68),
    ],
)
def test_predict(report: str, expected: int) -> None:
    """Test predict."""
    report = [int(r) for r in report.split()]
    assert predict(report) == expected


@pytest.mark.parametrize(
    ("report", "expected"),
    [
        ("0 3 6 9 12 15", -3),
        ("1 3 6 10 15 21", 0),
        ("10 13 16 21 30 45", 5),
    ],
)
def test_predict_reverse(report: str, expected: int) -> None:
    """Test predict in the reverse direction."""
    report = [int(r) for r in report.split()]
    assert predict(report, reverse=True) == expected


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 114


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 2
