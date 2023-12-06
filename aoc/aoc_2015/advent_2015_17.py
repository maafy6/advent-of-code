"""Advent of Code 2015 - Day 17

Day 17: No Such Thing as Too Much
=================================

The elves bought too much eggnog again - `150` liters this time. To fit it all
into your refrigerator, you'll need to move it into smaller containers. You
take an inventory of the capacities of the available containers.

For example, suppose you have containers of size `20`, `15`, `10`, `5`, and `5`
liters. If you need to store `25` liters, there are four ways to do it:

- `15` and `10`
- `20` and `5` (the first `5`)
- `20` and `5` (the second `5`)
- `15`, `5`, and `5`

Filling all containers entirely, how many different combinations of containers
can exactly fit all `150` liters of eggnog?

Part Two
========

While playing with all the containers in the kitchen, another load of eggnog
arrives! The shipping and receiving department is requesting as many containers
as you can spare.

Find the minimum number of containers that can exactly fit all `150` liters of
eggnog. How many different ways can you fill that number of containers and
still hold exactly `150` litres?

In the example above, the minimum number of containers was two. There were
three ways to use that many containers, and so the answer there would be `3`.
"""

import math
from typing import Iterator, Sequence, Tuple

from aocd import get_data

DATA = get_data(year=2015, day=17)


def partition_buckets(value: int, buckets: Sequence[int]) -> Iterator[Tuple[int, ...]]:
    """Yield partitions of the value into a list of fully filled buckets.

    :param value: The value to partition.
    :param buckets: The buckets available to partition the value.
    :yields: A tuple of buckets which sum to the value.
    """
    buckets = sorted(buckets)

    while buckets[-1] > value:
        buckets.pop()

    while sum(buckets) >= value:
        next_bucket = buckets.pop()
        if next_bucket == value:
            yield (next_bucket,)
        else:
            for partition in partition_buckets(value - next_bucket, buckets):
                partition += (next_bucket,)
                yield partition


def part1(data: str = DATA, qty: int = 150) -> int:
    """Solve part 1.

    :param data: The input data.
    :return: The number of ways to fill the buckets.
    """
    buckets = [int(b) for b in data.splitlines()]
    return len(list(partition_buckets(qty, buckets)))


def part2(data: str = DATA, qty: int = 150) -> int:
    """Solve part 2.

    :param data: The input data.
    :return: The number of ways to fill the buckets using the minimum number of containers..
    """
    buckets = [int(b) for b in data.splitlines()]

    min_containers = math.inf
    partitions = list(partition_buckets(qty, buckets))

    min_containers = min(len(p) for p in partitions)
    return len([p for p in partitions if len(p) == min_containers])
