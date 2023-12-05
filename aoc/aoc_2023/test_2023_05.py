"""Tests for AOC 2023-05."""

import math
from typing import Optional

import pytest

from .advent_2023_05 import Pipe, PipeRange, part1, part2


@pytest.fixture(name="data")
def _data() -> str:
    return """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
    """.strip()


@pytest.mark.parametrize(
    ("src", "expected"),
    [
        (0, 0),
        (1, 1),
        (48, 48),
        (49, 49),
        (50, 52),
        (51, 53),
        (96, 98),
        (97, 99),
        (98, 50),
        (99, 51),
    ],
)
def test_pipe(src: int, expected: int) -> None:
    """Test pipe input/outputs."""
    pipe = Pipe.loads(
        """
test-pipe map:
50 98 2
52 50 48
    """.strip()
    )

    assert pipe[src] == expected


@pytest.mark.parametrize(
    ("input_range", "expected"),
    [
        (PipeRange(0, math.inf, 0), PipeRange(56, 93, 0)),
        (PipeRange(0, 1, 0), None),
        (PipeRange(0, 69, 1), PipeRange(55, 69, 1)),
        (PipeRange(69, 100, 1), PipeRange(69, 92, 1)),
    ],
)
def test_feeder_range(input_range: PipeRange, expected: Optional[PipeRange]) -> None:
    """Test PipeRange.fed_from"""
    output_range = PipeRange(56, 93, 4)

    assert output_range.fed_from(input_range) == expected


def test_part_1(data: str) -> None:
    """Test part 1."""
    assert part1(data) == 35


def test_part_2(data: str) -> None:
    """Test part 2."""
    assert part2(data) == 46
