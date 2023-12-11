"""Tests for AOC 2023-10."""

from dataclasses import dataclass
from textwrap import dedent
from typing import Iterable

import pytest

from .advent_2023_10 import get_contained_tiles, parse_data, part1, part2


@dataclass
class FixtureParams:
    """Fixture parameters."""

    pipe_map: str
    points: Iterable[tuple[int, int]]


@pytest.fixture(
    name="part2_data",
    params=[
        (
            dedent(
                """\
                    ...........
                    .S-------7.
                    .|F-----7|.
                    .||.....||.
                    .||.....||.
                    .|L-7.F-J|.
                    .|..|.|..|.
                    .L--J.L--J.
                    ...........
                """
            ).strip(),
            [(6, 2), (6, 3), (6, 7), (6, 8)],
        ),
        (
            dedent(
                """\
                    ..........
                    .S------7.
                    .|F----7|.
                    .||....||.
                    .||....||.
                    .|L-7F-J|.
                    .|..||..|.
                    .L--JL--J.
                    ..........
                """
            ).strip(),
            [(6, 2), (6, 3), (6, 6), (6, 7)],
        ),
        (
            dedent(
                """\
                    .F----7F7F7F7F-7....
                    .|F--7||||||||FJ....
                    .||.FJ||||||||L7....
                    FJL7L7LJLJ||LJ.L-7..
                    L--J.L7...LJS7F-7L7.
                    ....F-J..F7FJ|L7L7L7
                    ....L7.F7||L7|.L7L7|
                    .....|FJLJ|FJ|F7|.LJ
                    ....FJL-7.||.||||...
                    ....L---J.LJ.LJLJ...
                """
            ).strip(),
            [(3, 14), (4, 7), (4, 8), (4, 9), (5, 7), (5, 8), (6, 6), (6, 14)],
        ),
        (
            dedent(
                """\
                    FF7FSF7F7F7F7F7F---7
                    L|LJ||||||||||||F--J
                    FL-7LJLJ||||||LJL-77
                    F--JF--7||LJLJ7F7FJ-
                    L---JF-JLJ.||-FJLJJ7
                    |F|F-JF---7F7-L7L|7|
                    |FFJF7L7F-JF7|JL---7
                    7-L-JL7||F7|L7F-7F7|
                    L.L7LFJ|||||FJL7||LJ
                    L7JLJL-JLJLJL--JLJ.L
                """
            ).strip(),
            [
                (3, 14),
                (4, 10),
                (4, 11),
                (4, 12),
                (4, 13),
                (5, 11),
                (5, 12),
                (5, 13),
                (6, 13),
                (6, 14),
            ],
        ),
    ],
)
def _part2_data(request: pytest.FixtureRequest) -> FixtureParams:
    return FixtureParams(*request.param)


@pytest.mark.parametrize(
    ("pipe_map", "expected"),
    [
        (
            dedent(
                """\
                    .....
                    .S-7.
                    .|.|.
                    .L-J.
                    .....
                """
            ).strip(),
            4,
        ),
        (
            dedent(
                """\
                    ..F7.
                    .FJ|.
                    SJ.L7
                    |F--J
                    LJ...
                """
            ).strip(),
            8,
        ),
    ],
)
def test_part_1(pipe_map: str, expected: int) -> None:
    """Test Part 1."""
    assert part1(pipe_map) == expected


def test_contained_tiles(part2_data: FixtureParams) -> None:
    """Test Part 2."""
    pipe_map = parse_data(part2_data.pipe_map)
    assert sorted(get_contained_tiles(pipe_map)) == sorted(part2_data.points)


def test_part_2(part2_data: FixtureParams) -> None:
    """Test Part 2."""
    assert part2(part2_data.pipe_map) == len(part2_data.points)
