"""Tests for AOC 2023-14."""

from textwrap import dedent

import pytest

from .advent_2023_14 import (
    calculate_load,
    parse_input,
    part1,
    part2,
    tilt_cycle,
    tilt_platform,
)


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        """\
            O....#....
            O.OO#....#
            .....##...
            OO.#O....O
            .O.....O#.
            O.#..O.#.#
            ..O..#O..O
            .......O..
            #....###..
            #OO..#....
        """
    ).strip()


def test_tilt_platform(data: str) -> None:
    """Test tilt platform."""
    platform = parse_input(data)
    expected = parse_input(
        dedent(
            """\
                ##....OOOO
                .......OOO
                ..OO#....O
                ......#..O
                .......O#.
                ##.#..O#.#
                .#....O#..
                .#.O#....O
                .....#....
                ...O#..O#.
            """
        ).strip()
    )

    assert tilt_platform(platform) == expected


@pytest.mark.parametrize(
    ("cycles", "expected"),
    [
        (
            1,
            dedent(
                """\
                    .....#....
                    ....#...O#
                    ...OO##...
                    .OO#......
                    .....OOO#.
                    .O#...O#.#
                    ....O#....
                    ......OOOO
                    #...O###..
                    #..OO#....
                """
            ).strip(),
        ),
        (
            2,
            dedent(
                """\
                    .....#....
                    ....#...O#
                    .....##...
                    ..O#......
                    .....OOO#.
                    .O#...O#.#
                    ....O#...O
                    .......OOO
                    #..OO###..
                    #.OOO#...O
              """
            ).strip(),
        ),
        (
            3,
            dedent(
                """\
                    .....#....
                    ....#...O#
                    .....##...
                    ..O#......
                    .....OOO#.
                    .O#...O#.#
                    ....O#...O
                    .......OOO
                    #...O###.O
                    #.OOO#...O
              """
            ).strip(),
        ),
    ],
)
def test_tilt_cycle(cycles: int, expected: str, data: str) -> None:
    """Test tilt_cycle."""
    platform = parse_input(data)
    expected = parse_input(expected)
    for _ in range(cycles):
        platform = tilt_cycle(platform)

    assert platform == expected


def test_calculate_load() -> None:
    """Test calculate load."""
    platform = parse_input(
        dedent(
            """\
                ##....OOOO
                .......OOO
                ..OO#....O
                ......#..O
                .......O#.
                ##.#..O#.#
                .#....O#..
                .#.O#....O
                .....#....
                ...O#..O#.
            """
        ).strip()
    )

    assert calculate_load(platform) == 136


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 136


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 64
