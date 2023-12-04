"""Tests for AOC 2015-17."""

import pytest

from .advent_2015_17 import part1, part2, partition_buckets


@pytest.fixture(name="containers")
def _containers() -> str:
    return """
20
15
10
5
5
    """.strip()


def test_partition_buckets() -> None:
    """Test partition_buckets."""
    assert sorted(partition_buckets(25, [20, 15, 10, 5, 5])) == sorted(
        [(10, 15), (5, 20), (5, 20), (5, 5, 15)]
    )


def test_part_1(containers: str) -> None:
    """Test part 1."""
    assert part1(containers, 25) == 4


def test_part_2(containers: str) -> None:
    """Test part 2."""
    assert part2(containers, 25) == 3
