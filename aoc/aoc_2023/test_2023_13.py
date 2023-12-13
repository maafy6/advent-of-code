"""Tests for AOC 2023-13."""

from textwrap import dedent

import pytest

from .advent_2023_13 import get_reflections, part1, part2


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        """\
        #.##..##.
        ..#.##.#.
        ##......#
        ##......#
        ..#.##.#.
        ..##..##.
        #.#.##.#.

        #...##..#
        #....#..#
        ..##..###
        #####.##.
        #####.##.
        ..##..###
        #....#..#
        """
    ).strip()


_mirrors = [
    [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ],
    [
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ],
]


@pytest.mark.parametrize(("mirror", "reflections"), zip(_mirrors, [(0, 5), (4, 0)]))
def test_get_reflections(mirror: list[str], reflections: tuple[int, int]) -> None:
    """Test get_reflections."""
    assert get_reflections(mirror) == reflections


@pytest.mark.parametrize(("mirror", "reflections"), zip(_mirrors, [(3, 0), (1, 0)]))
def test_get_reflections_with_smudge(
    mirror: list[str], reflections: tuple[int, int]
) -> None:
    """Test get_reflections."""
    assert get_reflections(mirror, 1) == reflections


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 405


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 400
