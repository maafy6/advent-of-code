"""Tests for AOC 2015-13."""

from typing import Mapping

import pytest

from .advent_2015_14 import Reindeer, reindeer_distance, reindeer_race, part1, part2


@pytest.fixture(name="reindeer")
def _reindeer() -> str:
    return """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
    """.strip()


@pytest.mark.parametrize(
    ("reindeer", "distance"),
    [
        (
            "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
            1120,
        ),
        (
            "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.",
            1056,
        ),
    ],
)
def test_reindeer_distance(reindeer: str, distance: int) -> None:
    """Test reindeer distance."""
    assert reindeer_distance(Reindeer.from_str(reindeer), time=1000) == distance


def test_part_1(reindeer: str) -> None:
    """Test part 1."""
    assert part1(reindeer, duration=1000) == 1120


@pytest.mark.parametrize(
    ("duration", "scores"),
    [
        (1, {"Dancer": 1}),
        (140, {"Dancer": 139, "Comet": 1}),
        (1000, {"Dancer": 689, "Comet": 312}),
    ],
)
def test_reindeer_race(reindeer: str, duration: int, scores: Mapping[str, int]) -> None:
    """Test reindeer_race."""
    reindeers = [Reindeer.from_str(desc) for desc in reindeer.split("\n")]
    assert reindeer_race(reindeers, duration) == scores


def test_part_2(reindeer: str) -> None:
    """Test part 2."""
    assert part2(reindeer, duration=1000) == 689
