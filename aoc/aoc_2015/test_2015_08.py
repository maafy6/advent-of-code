"""Tests for AOC 2015-08."""

import pytest

from .advent_2015_08 import get_encoding_lengths, get_lengths, part1, part2


@pytest.fixture(name="codes")
def _codes() -> str:
    return """
""
"abc"
"aaa\\"aaa"
"\\x27"
    """.strip()


@pytest.mark.parametrize(
    ("code", "code_len", "str_len"),
    [
        ('""', 2, 0),
        ('"abc"', 5, 3),
        ('"aaa\\"aaa"', 10, 7),
        ('"\\x27"', 6, 1),
    ],
)
def test_get_lengths(code: str, code_len: int, str_len: int) -> None:
    """Test get_difference."""
    assert get_lengths(code) == (code_len, str_len)


@pytest.mark.parametrize(
    ("code", "code_len", "str_len"),
    [
        ('""', 2, 6),
        ('"abc"', 5, 9),
        ('"aaa\\"aaa"', 10, 16),
        ('"\\x27"', 6, 11),
    ],
)
def test_get_encoding_lengths(code: str, code_len: int, str_len: int) -> None:
    """Test get_difference."""
    assert get_encoding_lengths(code) == (code_len, str_len)


def test_part_1(codes: str) -> None:
    """Test part 1."""
    assert part1(codes) == 12


def test_part_2(codes: str) -> None:
    """Test part 2."""
    assert part2(codes) == 19
