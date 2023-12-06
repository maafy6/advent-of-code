"""Advent of Code 2015 - Day 15

Day 15: Science for Hungry People
=================================

Today, you set out on the task of perfecting your milk-dunking cookie recipe.
All you have to do is find the right balance of ingredients.

Your recipe leaves room for exactly 100 teaspoons of ingredients. You make a
list of the remaining ingredients you could use to finish the recipe (your
puzzle input) and their properties per teaspoon:

- `capacity` (how well it helps the cookie absorb milk)
- `durability` (how well it keeps the cookie intact when full of milk)
- `flavor` (how tasty it makes the cookie)
- `texture` (how it improves the feel of the cookie)
- `calories` (how many calories it adds to the cookie)

You can only measure ingredients in whole-teaspoon amounts accurately, and you
have to be accurate so you can reproduce your results in the future. The total
score of a cookie can be found by adding up each of the properties (negative
totals become `0`) and then multiplying together everything except calories.

For instance, suppose you have these two ingredients:

```
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
```

Then, choosing to use `44` teaspoons of butterscotch and `56` teaspoons of
cinnamon (because the amounts of each ingredient must add up to `100`) would
result in a cookie with the following properties:

- A `capacity` of `44*-1 + 56*2 = 68`
- A `durability` of `44*-2 + 56*3 = 80`
- A `flavor` of `44*6 + 56*-2 = 152`
- A `texture` of `44*3 + 56*-1 = 76`

Multiplying these together (`68 * 80 * 152 * 76`, ignoring calories for now)
results in a total score of `62842880`, which happens to be the best score
possible given these ingredients. If any properties had produced a negative
total, it would have instead become zero, causing the whole score to multiply
to zero.

Given the ingredients in your kitchen and their properties, what is the total
score of the highest-scoring cookie you can make?

Part Two
========

Your cookie recipe becomes wildly popular! Someone asks if you can make another
recipe that has exactly `500` calories per cookie (so they can use it as a meal
replacement). Keep the rest of your award-winning process the same (`100`
teaspoons, same ingredients, same scoring system).

For example, given the ingredients above, if you had instead selected `40`
teaspoons of butterscotch and `60` teaspoons of cinnamon (which still adds to
`100`), the total calorie count would be `40*8 + 60*3 = 500`. The total score
would go down, though: only `57600000`, the best you can do in such trying
circumstances.

Given the ingredients in your kitchen and their properties, what is the total
score of the highest-scoring cookie you can make with a calorie total of `500`?
"""

import re
from dataclasses import dataclass
from itertools import permutations
from typing import Iterator, Mapping, Tuple

from aocd import get_data
from typing_extensions import Self

DATA = get_data(year=2015, day=15)


def partition(value: int, parts: int) -> Iterator[Tuple[int, ...]]:
    """Generate partitions of a number.

    :param value: The number to be partitioned.
    :param parts: The number of partition parts.
    :yields: A tuple partitioning the number into the number of parts.
        Some entries in the tuple may be 0, but the sum of the tuple will be
        `value`.
    """
    if parts == 1:
        yield (value,)
        return

    for i in range(1, value):
        for part in partition(value - i, parts - 1):
            yield (i,) + part

    # To catch all permutations including 0, generate partitions that are
    # smaller and yield all permutations with 0 filling in the missing slots.
    for part in partition(value, parts - 1):
        part += (0,)
        yield from permutations(part)


@dataclass
class Ingredient:
    """Ingredient model."""

    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    def __hash__(self) -> int:
        """Provide hash method."""
        return hash(self.name)

    @classmethod
    def from_desc(cls, desc: str) -> Self:
        """Create an ingredient from the description.

        :param desc: The ingredient description.
        :returns: The parsed ingredient.
        """
        name, prop_str = desc.split(":")
        props = {"name": name}
        for prop in re.finditer(
            r"(capacity|durability|flavor|texture|calories) (-?\d+)", prop_str
        ):
            props[prop.group(1)] = int(prop.group(2))

        return cls(**props)


def cookie_score(ingredients: Mapping[Ingredient, int]) -> int:
    """Return the score of a cookie.

    :param ingredients: A mapping of ingredients to their weight in the cookie.
    :returns: The score of the cookie.
    """
    score = 1
    for prop in ("capacity", "durability", "flavor", "texture"):
        score *= max(
            sum(
                getattr(ingredient, prop) * weight
                for ingredient, weight in ingredients.items()
            ),
            0,
        )

    return score


def cookie_calories(ingredients: Mapping[Ingredient, int]) -> int:
    """Determine the number of calories in the cookie.

    :param ingredients: A mapping of ingredients to their weight in the cookie.
    :returns: The number of calories.
    """
    return sum(
        ingredient.calories * weight for ingredient, weight in ingredients.items()
    )


def part1(data: str = DATA) -> int:
    """Solve part 1.

    :param data: The input data.
    :returns: The highest scoring cookie.
    """
    ingredients = [Ingredient.from_desc(desc) for desc in data.splitlines()]

    score = 0
    for part in partition(100, len(ingredients)):
        cookie = dict(zip(ingredients, part))
        score = max(score, cookie_score(cookie))

    return score


def part2(data: str = DATA) -> int:
    """Solve part 2.

    :param data: The input data.
    :returns: The highest scoring cookie.
    """
    ingredients = [Ingredient.from_desc(desc) for desc in data.splitlines()]

    score = 0
    for part in partition(100, len(ingredients)):
        cookie = dict(zip(ingredients, part))
        if cookie_calories(cookie) != 500:
            continue
        score = max(score, cookie_score(cookie))

    return score
