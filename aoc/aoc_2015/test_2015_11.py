"""Tests for AOC 2015-11."""


import pytest

from .advent_2015_11 import Password


@pytest.mark.parametrize(
    ("password", "expected"),
    [
        ("xx", "xy"),
        ("xy", "xz"),
        ("xz", "ya"),
        ("ya", "yb"),
    ],
)
def test_increment_password(password: str, expected: str) -> None:
    """Test increment_password."""
    assert Password(password).increment() == expected


@pytest.mark.parametrize(
    ("password", "is_valid"),
    [
        ("hijklmmn", False),
        ("abbceffg", False),
        ("abbcegjk", False),
        ("abcdffaa", True),
        ("ghjaabcc", True),
        ("ghjaabcb", False),
    ],
)
def test_is_valid_password(password: str, is_valid: bool) -> None:
    """Test is_valid_password."""
    assert Password(password).is_valid() is is_valid


@pytest.mark.parametrize(
    ("password", "expected"),
    [
        ("abcdefgh", "abcdffaa"),
        ("ghijklmn", "ghjaabcc"),
    ],
)
def test_next_valid_password(password: str, expected: str) -> None:
    """Test increment_password."""
    assert Password(password).next_valid() == expected
