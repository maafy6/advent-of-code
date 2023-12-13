"""Tests for AOC 2023-12."""

from textwrap import dedent

import pytest

from .advent_2023_12 import (
    count_expanded_nonogram,
    count_nonograms,
    gen_nonograms,
    part1,
    part2,
)


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
        ("???.###", (1, 1, 3), ["#.#.###"]),
        (
            ".??..??...?##.",
            (1, 1, 3),
            [
                "..#...#...###.",
                "..#..#....###.",
                ".#....#...###.",
                ".#...#....###.",
            ],
        ),
        ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), [".#.###.#.######"]),
        ("????.#...#...", (4, 1, 1), ["####.#...#..."]),
        (
            "????.######..#####.",
            (1, 6, 5),
            [
                "...#.######..#####.",
                "..#..######..#####.",
                ".#...######..#####.",
                "#....######..#####.",
            ],
        ),
        (
            "?###????????",
            (3, 2, 1),
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


@pytest.mark.parametrize(
    ("record", "desc", "count"),
    [
        ("???.###", (1, 1, 3), 1),
        (".??..??...?##.", (1, 1, 3), 4),
        ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
        ("????.#...#...", (4, 1, 1), 1),
        ("????.######..#####.", (1, 6, 5), 4),
        ("?###????????", (3, 2, 1), 10),
    ],
)
def test_count_nonograms(record: str, desc: list[int], count: int) -> None:
    """Test count_nonograms."""
    assert count_nonograms(record, desc) == count


@pytest.mark.parametrize(
    ("record", "desc", "count"),
    [
        ("???.###", (1, 1, 3), 1),
        (".??..??...?##.", (1, 1, 3), 16384),
        ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
        ("????.#...#...", (4, 1, 1), 16),
        ("????.######..#####.", (1, 6, 5), 2500),
        ("?###????????", (3, 2, 1), 506250),
    ],
)
def test_count_expanded_nonograms(record: str, desc: list[int], count: int) -> None:
    """Test count_expanded_nonogram."""
    assert count_expanded_nonogram(record, desc, 5) == count


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 21


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 525152
