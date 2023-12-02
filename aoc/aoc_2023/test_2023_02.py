"""Tests for AOC 2023-02."""

import pytest

from .advent_2023_02 import minimum_power, part1, part2


@pytest.fixture(name="game_logs")
def _game_logs() -> str:
    return """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """.strip()


@pytest.mark.parametrize(
    ("results", "power"),
    [
        ("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", 48),
        ("1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", 12),
        ("8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", 1560),
        ("1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", 630),
        ("6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", 36),
    ],
)
def test_get_minimum_power(results: str, power: int) -> None:
    """Test minimum_power."""
    assert minimum_power(results) == power


def test_part_1(game_logs: str) -> None:
    """Test part1."""
    assert part1(game_logs) == 8


def test_part_2(game_logs: str) -> None:
    """Test part2."""
    assert part2(game_logs) == 2286
