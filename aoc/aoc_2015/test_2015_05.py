"""Tests for AOC 2015-05."""

import pytest

from .advent_2015_05 import is_nice_part_1, is_nice_part_2, part1, part2


@pytest.mark.parametrize(
    ("string", "nice"),
    [
        ("ugknbfddgicrmopn", True),
        ("aaa", True),
        ("jchzalrnumimnmhp", False),
        ("haegwjzuvuyypxyu", False),
        ("dvszwmarrgswjxmb", False),
    ],
)
def test_is_nice_part_1(string: str, nice: int) -> None:
    """Test is_nice."""
    assert is_nice_part_1(string) is nice


def test_part_1() -> None:
    """Test part 1."""
    word_list = """
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
    """.strip()

    assert part1(word_list) == 2


@pytest.mark.parametrize(
    ("string", "nice"),
    [
        ("qjhvhtzxzqqjkmpb", True),
        ("xxyxx", True),
        ("uurcxstgmygtbstg", False),
        ("ieodomkazucvgmuy", False),
        ("xyxy", True),
        ("aaa", False),
    ],
)
def test_is_nice_part_2(string: str, nice: int) -> None:
    """Test is_nice."""
    assert is_nice_part_2(string) is nice


def test_part_2() -> None:
    """Test part 2."""
    word_list = """
qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy
    """.strip()

    assert part2(word_list) == 2
