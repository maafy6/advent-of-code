"""Tests for AOC 2015-12."""

from typing import Any, Sequence

import pytest

from .advent_2015_12 import gen_numbers, part1, part2


@pytest.mark.parametrize(
    ("doc", "numbers"),
    [
        ([1, 2, 3], [1, 2, 3]),
        ({"a": 2, "b": 4}, [2, 4]),
        ([[[3]]], [3]),
        ({"a": {"b": 4}, "c": -1}, [4, -1]),
        ({"a": [-1, 1]}, [-1, 1]),
        ([-1, {"a": 1}], [-1, 1]),
        ([], []),
        ({}, []),
    ],
)
def test_gen_numbers(doc: Any, numbers: Sequence[int]) -> None:
    """Test gen_numbers."""
    assert sorted(gen_numbers(doc)) == sorted(numbers)


@pytest.mark.parametrize(
    ("doc", "numbers"),
    [
        ([1, 2, 3], [1, 2, 3]),
        ([1, {"c": "red", "b": 2}, 3], [1, 3]),
        ({"d": "red", "e": [1, 2, 3, 4], "f": 5}, []),
        ([1, "red", 5], [1, 5]),
    ],
)
def test_gen_numbers_filtered(doc: Any, numbers: Sequence[int]) -> None:
    """Test gen_numbers."""
    assert sorted(gen_numbers(doc, filters=["red"])) == sorted(numbers)


@pytest.mark.parametrize(
    ("doc", "total"),
    [
        ("""[1,2,3]""", 6),
        ("""{"a":2,"b":4}""", 6),
        ("""[[[3]]]""", 3),
        ("""{"a":{"b":4},"c":-1}""", 3),
        ("""{"a":[-1,1]}""", 0),
        ("""[-1,{"a":1}]""", 0),
        ("""[]""", 0),
        ("""{}""", 0),
    ],
)
def test_part_1(doc: str, total: int) -> None:
    """Test part 1."""
    assert part1(doc) == total


@pytest.mark.parametrize(
    ("doc", "total"),
    [
        ("""[1, 2, 3]""", 6),
        ("""[1, {"c": "red", "b": 2}, 3]""", 4),
        ("""{"d": "red", "e": [1, 2, 3, 4], "f": 5}""", 0),
        ("""[1, "red", 5]""", 6),
    ],
)
def test_part_2(doc: str, total: int) -> None:
    """Test part 1."""
    assert part2(doc) == total
