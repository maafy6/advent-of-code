"""Tests for AOC 2015-15."""

from typing import Mapping

import pytest

from .advent_2015_15 import (
    Ingredient,
    cookie_calories,
    cookie_score,
    partition,
    part1,
    part2,
)


def test_partition():
    """Test the partition generator."""
    assert set(partition(4, 3)) == {
        (4, 0, 0),
        (0, 4, 0),
        (0, 0, 4),
        (3, 1, 0),
        (3, 0, 1),
        (0, 3, 1),
        (2, 2, 0),
        (2, 0, 2),
        (0, 2, 2),
        (1, 3, 0),
        (1, 0, 3),
        (0, 1, 3),
        (2, 1, 1),
        (1, 2, 1),
        (1, 1, 2),
    }


@pytest.fixture(name="ingredients")
def _ingredients() -> str:
    return """
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
    """.strip()


@pytest.mark.parametrize(
    ("ingredient_weights", "score"),
    [
        ({"Butterscotch": 44, "Cinnamon": 56}, 62842880),
        ({"Butterscotch": 100}, 0),
    ],
)
def test_cookie_score(
    ingredients: str, ingredient_weights: Mapping[str, int], score: int
) -> None:
    """Test cookie_score."""
    ingreds = {
        desc.split(":")[0]: Ingredient.from_desc(desc)
        for desc in ingredients.split("\n")
    }
    cookie = {
        ingreds[ingredient]: weight for ingredient, weight in ingredient_weights.items()
    }
    assert cookie_score(cookie) == score


def test_part_1(ingredients: str) -> None:
    """Test part 1."""
    assert part1(ingredients) == 62842880


@pytest.mark.parametrize(
    ("ingredient_weights", "calories"),
    [({"Butterscotch": 40, "Cinnamon": 60}, 500)],
)
def test_cookie_calories(
    ingredients: str, ingredient_weights: Mapping[str, int], calories: int
) -> None:
    """Test cookie_calories."""
    ingreds = {
        desc.split(":")[0]: Ingredient.from_desc(desc)
        for desc in ingredients.split("\n")
    }
    cookie = {
        ingreds[ingredient]: weight for ingredient, weight in ingredient_weights.items()
    }
    assert cookie_calories(cookie) == calories


def test_part_2(ingredients: str) -> None:
    """Test part 2."""
    assert part2(ingredients) == 57600000
