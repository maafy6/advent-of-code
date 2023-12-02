"""Tests for AOC 2015-06."""

from typing import Tuple

import pytest

from .advent_2015_06 import parse_instruction, part1, part2


@pytest.mark.parametrize(
    ("instruction", "command", "corner1", "corner2"),
    [
        ("turn on 0,0 through 999,999", "turn on", (0, 0), (999, 999)),
        ("toggle 0,0 through 999,0", "toggle", (0, 0), (999, 0)),
        ("turn off 499,499 through 500,500", "turn off", (499, 499), (500, 500)),
    ],
)
def test_parse_instruction(
    instruction: str, command: str, corner1: Tuple[int, int], corner2: Tuple[int, int]
) -> None:
    """Test parse_instruaction."""
    assert parse_instruction(instruction) == (command, corner1, corner2)


@pytest.mark.parametrize(
    ("instructions", "count"),
    [
        ("turn on 0,0 through 999,999", 1_000_000),
        ("turn on 0,0 through 999,999\ntoggle 0,0 through 999,0", 999_000),
        (
            """
            turn on 0,0 through 999,999
            toggle 0,0 through 999,0
            turn off 499,499 through 500,500
            """,
            998_996,
        ),
    ],
)
def test_part_1(instructions: str, count: int) -> None:
    """Test part1."""
    assert part1(instructions) == count


@pytest.mark.parametrize(
    ("instructions", "brightness"),
    [
        ("turn on 0,0 through 0,0", 1),
        ("turn on 0,0 through 0,0\ntoggle 0,0 through 999,999", 2_000_001),
    ],
)
def test_part_2(instructions: str, brightness: int) -> None:
    """Test part2."""
    assert part2(instructions) == brightness
