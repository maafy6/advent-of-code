"""Tests for AOC 2023-08."""

from textwrap import dedent

import pytest

from .advent_2023_08 import part1, part2


@pytest.fixture(
    name="data",
    params=[
        (
            dedent(
                """\
        RL

        AAA = (BBB, CCC)
        BBB = (DDD, EEE)
        CCC = (ZZZ, GGG)
        DDD = (DDD, DDD)
        EEE = (EEE, EEE)
        GGG = (GGG, GGG)
        ZZZ = (ZZZ, ZZZ)
        """
            ).strip(),
            2,
        ),
        (
            dedent(
                """\
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
            """
            ).strip(),
            6,
        ),
    ],
)
def _data(request: pytest.FixtureRequest) -> tuple[str, int]:
    return request.param


def test_part_1(data: tuple[str, int]) -> None:
    """Test Part 1."""
    desert_map, expected = data
    assert part1(desert_map) == expected


def test_part_2() -> None:
    """Test Part 2."""
    data = dedent(
        """
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
        """
    ).strip()

    assert part2(data) == 6
