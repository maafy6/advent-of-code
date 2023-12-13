"""Tests for AOC 2023-12."""

from textwrap import dedent

import pytest

from .advent_2023_12 import gen_nonograms, part1, part2


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        """\
            ???.### 1,1,3
            .??..??...?##. 1,1,3
            ?#?#?#?#?#?#?#? 1,3,1,6
            ????.#...#... 4,1,1
            ????.######..#####. 1,6,5
            ?###???????? 3,2,1
        """
    ).strip()


@pytest.mark.parametrize(
    ("record", "desc", "nonograms"),
    [
        ("???.###", [1, 1, 3], ["#.#.###"]),
        (
            ".??..??...?##.",
            [1, 1, 3],
            [
                "..#...#...###.",
                "..#..#....###.",
                ".#....#...###.",
                ".#...#....###.",
            ],
        ),
        ("?#?#?#?#?#?#?#?", [1, 3, 1, 6], [".#.###.#.######"]),
        ("????.#...#...", [4, 1, 1], ["####.#...#..."]),
        (
            "????.######..#####.",
            [1, 6, 5],
            [
                "...#.######..#####.",
                "..#..######..#####.",
                ".#...######..#####.",
                "#....######..#####.",
            ],
        ),
        (
            "?###????????",
            [3, 2, 1],
            [
                ".###....##.#",
                ".###...##..#",
                ".###...##.#.",
                ".###..##...#",
                ".###..##..#.",
                ".###..##.#..",
                ".###.##....#",
                ".###.##...#.",
                ".###.##..#..",
                ".###.##.#...",
            ],
        ),
    ],
)
def test_gen_nonograms(record: str, desc: list[int], nonograms: list[str]) -> None:
    """Test gen_nonograms."""
    assert sorted(list(gen_nonograms(record, desc))) == sorted(nonograms)


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 21


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 525152
