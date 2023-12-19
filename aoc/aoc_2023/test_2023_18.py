"""Tests for AOC 2023-18."""

from textwrap import dedent

import pytest

from .advent_2023_18 import Polygon, part1, part2


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        """
            R 6 (#70c710)
            D 5 (#0dc571)
            L 2 (#5713f0)
            D 2 (#d2c081)
            R 2 (#59c680)
            D 2 (#411b91)
            L 5 (#8ceee2)
            U 2 (#caa173)
            L 1 (#1b58a2)
            U 2 (#caa171)
            R 2 (#7807d2)
            U 3 (#a77fa3)
            L 2 (#015232)
            U 2 (#7a21e3)
        """
    ).strip()


@pytest.mark.parametrize(
    ("data", "count"),
    [
        (
            dedent(
                """
                    R 6 (#70c710)
                    D 5 (#0dc571)
                    L 2 (#5713f0)
                    D 2 (#d2c081)
                    R 2 (#59c680)
                    D 2 (#411b91)
                    L 5 (#8ceee2)
                    U 2 (#caa173)
                    L 1 (#1b58a2)
                    U 2 (#caa171)
                    R 2 (#7807d2)
                    U 3 (#a77fa3)
                    L 2 (#015232)
                    U 2 (#7a21e3)
                """
            ).strip(),
            62,
        ),
        (
            dedent(
                """
                    R 6 (#000060)
                    D 6 (#000061)
                    L 2 (#000022)
                    U 3 (#000033)
                    L 2 (#000022)
                    D 3 (#000031)
                    L 2 (#000022)
                    U 6 (#000063)
                """
            ).strip(),
            46,
        ),
        (
            dedent(
                """
                    R 2 (#000020)
                    D 3 (#000031)
                    R 2 (#000020)
                    U 3 (#000033)
                    R 2 (#000020)
                    D 6 (#000061)
                    L 6 (#000062)
                    U 6 (#000063)
                """
            ).strip(),
            46,
        ),
    ],
)
def test_count(data: str, count: int) -> None:
    """Test count."""
    poly = Polygon.loads(data, part=1)
    assert poly.count() == count


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 62


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 952408144115
