"""Tests for AOC 2015-18."""

import pytest

from .advent_2015_18 import LightGrid, part1, part2


@pytest.mark.parametrize(
    ("before", "after"),
    [
        (
            """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
            """,
            """
..##..
..##.#
...##.
......
#.....
#.##..
            """,
        ),
        (
            """
..##..
..##.#
...##.
......
#.....
#.##..
            """,
            """
..###.
......
..###.
......
.#....
.#....
            """,
        ),
        (
            """
..###.
......
..###.
......
.#....
.#....
            """,
            """
...#..
......
...#..
..##..
......
......
            """,
        ),
        (
            """
......
......
..##..
..##..
......
......
            """,
            """
......
......
..##..
..##..
......
......
            """,
        ),
    ],
)
def test_animate(before: str, after: str) -> None:
    """Test animate."""
    initial = LightGrid.from_text(before.strip())
    animated = initial.animate()

    assert str(animated) == after.strip()


@pytest.mark.parametrize(
    ("before", "after"),
    [
        (
            """
##.#.#
...##.
#....#
..#...
#.#..#
####.#
            """,
            """
#.##.#
####.#
...##.
......
#...#.
#.####
            """,
        ),
        (
            """
#.##.#
####.#
...##.
......
#...#.
#.####
            """,
            """
#..#.#
#....#
.#.##.
...##.
.#..##
##.###
            """,
        ),
        (
            """
#..#.#
#....#
.#.##.
...##.
.#..##
##.###
            """,
            """
#...##
####.#
..##.#
......
##....
####.#
            """,
        ),
        (
            """
#...##
####.#
..##.#
......
##....
####.#
            """,
            """
#.####
#....#
...#..
.##...
#.....
#.#..#
            """,
        ),
        (
            """
#.####
#....#
...#..
.##...
#.....
#.#..#
            """,
            """
##.###
.##..#
.##...
.##...
#.#...
##...#
            """,
        ),
    ],
)
def test_animate_corners_on(before: str, after: str) -> None:
    """Test animate."""
    initial = LightGrid.from_text(before.strip(), corners_on=True)
    animated = initial.animate()

    assert str(animated) == after.strip()


def test_lit() -> None:
    """Test lit."""
    grid = LightGrid.from_text(
        """
......
......
..##..
..##..
......
......
        """.strip()
    )

    assert grid.lit == 4


def test_part_1() -> None:
    """Test part 1."""
    initial = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
    """.strip()

    assert part1(initial, 4) == 4


def test_part_2() -> None:
    """Test part 2."""
    initial = """
##.#.#
...##.
#....#
..#...
#.#..#
####.#
    """.strip()

    assert part2(initial, 5) == 17
