"""Advent of Code 2015 - Day 12

Day 12: JSAbacusFramework.io
============================

Santa's Accounting-Elves need help balancing the books after a recent order.
Unfortunately, their accounting software uses a peculiar storage format. That's
where you come in.

They have a JSON document which contains a variety of things: arrays
(`[1,2,3]`), objects (`{"a":1, "b":2}`), numbers, and strings. Your first job
is to simply find all of the numbers throughout the document and add them
together.

For example:

- `[1,2,3]` and `{"a":2,"b":4}` both have a sum of `6`.
- `[[[3]]]` and `{"a":{"b":4},"c":-1}` both have a sum of `3`.
- `{"a":[-1,1]}` and `[-1,{"a":1}]` both have a sum of `0`.
- `[]` and `{}` both have a sum of `0`.

You will not encounter any strings containing numbers.

What is the sum of all numbers in the document?

Part Two
========

Uh oh - the Accounting-Elves have realized that they double-counted everything
red.

Ignore any object (and all of its children) which has any property with the
value `"red"`. Do this only for objects (`{...}`), not arrays (`[...]`).

- `[1,2,3]` still has a sum of `6`.
- `[1,{"c":"red","b":2},3]` now has a sum of `4`, because the middle object is
    ignored.
- `{"d":"red","e":[1,2,3,4],"f":5}` now has a sum of `0`, because the entire
    structure is ignored.
- `[1,"red",5]` has a sum of `6`, because `"red"` in an array has no effect.
"""

import json
from typing import Any, Iterator, Optional, Sequence

from aocd import get_data

DATA = get_data(year=2015, day=12)


def gen_numbers(doc: Any, filters: Optional[Sequence[str]] = None) -> Iterator[int]:
    """Yield the numbers from the document."""
    if isinstance(doc, dict):
        if filters and any(f in doc.values() for f in filters):
            return

        for val in doc.values():
            yield from gen_numbers(val, filters=filters)
    elif isinstance(doc, list):
        for val in doc:
            yield from gen_numbers(val, filters=filters)
    elif isinstance(doc, int):
        yield doc


def part1(data: str = DATA) -> int:
    """Solve Part 1.

    :param data: The input data.
    :returns: The sum of all numbers in the document.
    """
    data = json.loads(data)
    return sum(gen_numbers(data))


def part2(data: str = DATA) -> int:
    """Solve Part 2.

    :param data: The input data.
    :returns: The sum of all numbers in the filtered document.
    """
    data = json.loads(data)
    return sum(gen_numbers(data, filters=["red"]))
