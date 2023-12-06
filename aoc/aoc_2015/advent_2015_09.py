"""Advent of Code 2015 - Day 9

Day 9: All in a Single Night
============================

Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit; his elves have provided
him the distances between every pair of locations. He can start and end at any
two (different) locations he wants, but he must visit each location exactly
once. What is the shortest distance he can travel to achieve this?

For example, given the following distances:

```
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
```

The possible routes are therefore:

```
Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982
```

The shortest of these is `London -> Dublin -> Belfast = 605`, and so the answer
is `605` in this example.

What is the distance of the shortest route?

Part Two
========

The next year, just to show off, Santa decides to take the route with the
longest distance instead.

He can still start and end at any two (different) locations he wants, and he
still must visit each location exactly once.

For example, given the distances above, the longest route would be `982` via
(for example) `Dublin -> London -> Belfast`.

What is the distance of the longest route?
"""

import math
from collections import defaultdict
from copy import copy
from typing import Mapping, Optional, MutableSequence, Iterator, Tuple

from aocd import get_data

DATA = get_data(year=2015, day=9)


def get_distances(data: str) -> Mapping[str, Mapping[str, int]]:
    """Build a bi-directional mapping indicating distances between each pair.

    :param data: The distances data.
    :returns: The distance mapping.
    """
    distances = defaultdict(lambda: defaultdict(int))
    for line in data.splitlines():
        route_desc, distance = line.split(" = ")
        place1, place2 = route_desc.split(" to ")
        distance = int(distance)

        distances[place1][place2] = distance
        distances[place2][place1] = distance

    return distances


def gen_routes(
    nodes: MutableSequence[str],
    distances: Mapping[str, Mapping[str, int]],
    *,
    route: Optional[MutableSequence[str]] = None,
    route_score: int = 0,
    min_dist: Optional[int] = math.inf,
) -> Iterator[Tuple[MutableSequence[str], int]]:
    """Generate routes traversing all nodes.

    :param nodes: A list of untraversed nodes.
    :param distances: A mapping of distances between nodes.
    :min_dist: If specified, filter routes longer than this distance.
    :route: The current route as traversed so far.
    :route_score: The distance traversed by the current route.
    """
    if not nodes:
        yield route, route_score

    if not route:
        route = []

    for node in nodes:
        if route:
            sub_route_score = route_score + distances[route[-1]][node]
        else:
            sub_route_score = 0

        if sub_route_score > min_dist:
            continue

        sub_nodes = copy(nodes)
        sub_nodes.remove(node)
        sub_route = copy(route)
        sub_route.append(node)

        yield from gen_routes(
            sub_nodes,
            distances,
            route=sub_route,
            route_score=sub_route_score,
            min_dist=min_dist,
        )


def part1(data: str = DATA) -> int:
    """Solve part 1.

    :param data: The distance map.
    :returns: The minimum traversal distance.
    """
    distances = get_distances(data)
    nodes = sorted(list(distances.keys()))

    min_dist = math.inf
    for _, dist in gen_routes(nodes, distances, min_dist=min_dist):
        if dist < min_dist:
            min_dist = dist

    return min_dist


def part2(data: str = DATA) -> int:
    """Solve part 2.

    :param data: The distance map.
    :returns: The maximum traversal distance.
    """
    distances = get_distances(data)
    nodes = sorted(list(distances.keys()))

    max_dist = 0
    for _, dist in gen_routes(nodes, distances):
        if dist > max_dist:
            max_dist = dist

    return max_dist
