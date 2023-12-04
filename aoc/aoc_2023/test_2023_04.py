"""Tests for AOC 2023-04."""

from dataclasses import dataclass
from typing import Sequence

import pytest

from .advent_2023_04 import gen_cards, part1, part2, score_scratcher


@dataclass
class CardData:
    """Card fixtrure model."""

    winning: Sequence[str]
    numbers: Sequence[str]
    score: int
    matching: int


@pytest.fixture(name="cards")
def _cards() -> str:
    return """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    """.strip()


@pytest.fixture(
    name="card_data",
    params=[
        ("41 48 83 86 17".split(" "), "83 86 6 31 17 9 48 53".split(" "), 8, 4),
        ("13 32 20 16 61".split(" "), "61 30 68 82 17 32 24 19".split(" "), 2, 2),
        ("1 21 53 59 44".split(" "), "69 82 63 72 16 21 14 1".split(" "), 2, 2),
        ("41 92 73 84 69".split(" "), "59 84 76 51 58 5 54 83".split(" "), 1, 1),
        ("87 83 26 28 32".split(" "), "88 30 70 12 93 22 82 36".split(" "), 0, 0),
        ("31 18 13 56 72".split(" "), "74 77 10 23 35 67 36 11".split(" "), 0, 0),
    ],
)
def _card_data(request: pytest.FixtureRequest) -> CardData:
    return CardData(*request.param)


def test_gen_cards() -> None:
    """Test gen_cards."""
    assert list(gen_cards("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")) == [
        ("41 48 83 86 17".split(" "), "83 86 6 31 17 9 48 53".split(" "))
    ]


@pytest.mark.parametrize("count", [True, False])
def test_score_scratcher(card_data: CardData, count: bool) -> None:
    """Test score_scratcher."""
    assert score_scratcher(card_data.winning, card_data.numbers, count=count) == (
        card_data.matching if count else card_data.score
    )


def test_part_1(cards: str) -> None:
    """Test part 1."""
    assert part1(cards) == 13


def test_part_2(cards: str) -> None:
    """Test part 2."""
    assert part2(cards) == 30
