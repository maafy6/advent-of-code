"""Advent of Code 2023: Day 17

Day 17: Clumsy Crucible
=======================

The lava starts flowing rapidly once the Lava Production Facility is
operational. As you leave, the reindeer offers you a parachute, allowing you to
quickly reach Gear Island.

As you descend, your bird's-eye view of Gear Island reveals why you had trouble
finding anyone on your way up: half of Gear Island is empty, but the half below
you is a giant factory city!

You land near the gradually-filling pool of lava at the base of your new
lavafall. Lavaducts will eventually carry the lava throughout the city, but to
make use of it immediately, Elves are loading it into large crucibles on wheels.

The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles
become very difficult to steer at high speeds, and so it can be hard to go in a
straight line for very long.

To get Desert Island the machine parts it needs as soon as possible, you'll need
to find the best way to get the crucible from the lava pool to the machine parts
factory. To do this, you need to minimize heat loss while choosing a route that
doesn't require the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic
patterns, ambient temperature, and hundreds of other parameters to calculate
exactly how much heat loss can be expected for a crucible entering any
particular city block.

For example:

```
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
```

Each city block is marked by a single digit that represents the amount of heat
loss if the crucible enters that block. The starting point, the lava pool, is
the top-left city block; the destination, the machine parts factory, is the
bottom-right city block. (Because you already start in the top-left block, you
don't incur that block's heat loss unless you leave that block and then return
to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line
for very long, it can move at most three blocks in a single direction before it
must turn 90 degrees left or right. The crucible also can't reverse direction;
after entering each city block, it may only turn left, continue straight, or
turn right.

One way to minimize heat loss is this path:

```
2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
```

This path never moves more than three consecutive blocks in the same direction
and incurs a heat loss of only `102`.

Directing the crucible from the lava pool to the machine parts factory, but not
moving more than three consecutive blocks in the same direction, what is the
least heat loss it can incur?

Part Two
========

The crucibles of lava simply aren't large enough to provide an adequate supply
of lava to the machine parts factory. Instead, the Elves are going to upgrade to
ultra crucibles.

Ultra crucibles are even more difficult to steer than normal crucibles. Not only
do they have trouble going in a straight line, but they also have trouble
turning!

Once an ultra crucible starts moving in a direction, it needs to move a minimum
of four blocks in that direction before it can turn (or even before it can stop
at the end). However, it will eventually start to get wobbly: an ultra crucible
can move a maximum of ten consecutive blocks without turning.

In the above example, an ultra crucible could follow this path to minimize heat
loss:

```
2>>>>>>>>1323
32154535v5623
32552456v4254
34465858v5452
45466578v>>>>
143859879845v
445787698776v
363787797965v
465496798688v
456467998645v
122468686556v
254654888773v
432267465553v
```

In the above example, an ultra crucible would incur the minimum possible heat
loss of `94`.

Here's another example:

```
111111111111
999999999991
999999999991
999999999991
999999999991
```

Sadly, an ultra crucible would need to take an unfortunate path like this one:

```
1>>>>>>>1111
9999999v9991
9999999v9991
9999999v9991
9999999v>>>>
```

This route causes the ultra crucible to incur the minimum possible heat loss of
`71`.

Directing the ultra crucible from the lava pool to the machine parts factory,
what is the least heat loss it can incur?
"""

import math
from collections import defaultdict
from queue import PriorityQueue
from typing import Literal

from aocd import get_data

DATA = get_data(year=2023, day=17)

Direction = Literal["N", "S", "E", "W"]
Point = tuple[int, int, Direction | None]


def parse_input(data: str) -> tuple[tuple[int]]:
    """Parse the input."""
    return tuple(tuple(int(n) for n in line) for line in data.splitlines())


def get_neighbors(
    grid: tuple[tuple[int]],
    pos: tuple[int, int],
    direction: Direction | None = None,
    min_dist: int = 1,
    max_dist: int | None = None,
) -> tuple[Point]:
    """Return the neighbors that can be travelled to.

    :param grid: The grid map.
    :param pos: The current position.
    :param direction: The last direction travelled.
    :param min_dist: The minimum distance that must be travelled.
    :param max_dist: The maximum distance that can be travelled.
    :returns: A tuple of points that can be reached from this node.
    """
    neighbors = []
    grid_size = (len(grid), len(grid[0]))
    for d in range(min_dist, (max_dist + 1) or max(grid_size)):
        if direction is None or direction in "EW":
            neighbors.append((pos[0] - d, pos[1], "N"))
            neighbors.append((pos[0] + d, pos[1], "S"))
        if direction is None or direction in "NS":
            neighbors.append((pos[0], pos[1] + d, "E"))
            neighbors.append((pos[0], pos[1] - d, "W"))

    return tuple(
        (i, j, d)
        for i, j, d in neighbors
        if 0 <= i < grid_size[0] and 0 <= j < grid_size[1]
    )


def a_star(
    grid: tuple[tuple[int]], min_dist: int = 1, max_dist: int | None = None
) -> int:
    """Perform the A* search algorithm on the grid map.

    This finds the cheapest path from the starting point `(0,0)` to the exit
    `(len(grid)-1, len(grid[0])-1)`.

    :param grid: The grid map.
    :param min_dist: The minimum distance that must be travelled in a given
        direction.
    :param max_dist: The maximum distance that can be travelled in a given
        direction.
    :returns: The score of the cheapest path through the grid.
    :raises ValueError: If a path cannot be found through the grid.
    """
    goal = (len(grid) - 1, len(grid[0]) - 1)

    # The queue of nodes to be checked, ordered by their current cheapest cost
    # from the starting node. Cheapest entries are retrieved first.
    unsolved = PriorityQueue()
    unsolved.put((0, (0, 0, None)))

    # A map of points (and the direction they are reached from) to their score.
    # Need to store the direction travelled to reach them as well, as different
    # paths may pass through the same node in different directions, yielding
    # different paths.
    scores = defaultdict(lambda: math.inf)
    scores[(0, 0, None)] = 0

    while unsolved:
        score, closest_point = unsolved.get()
        current, direction = closest_point[:2], closest_point[2]
        if current == goal:
            return score

        for n in get_neighbors(grid, current, direction, min_dist, max_dist):
            cost = 0
            if n[2] == "N":
                cost = sum(grid[i][n[1]] for i in range(n[0], current[0]))
            elif n[2] == "S":
                cost = sum(grid[i][n[1]] for i in range(current[0] + 1, n[0] + 1))
            elif n[2] == "E":
                cost = sum(grid[n[0]][current[1] + 1 : n[1] + 1])
            elif n[2] == "W":
                cost = sum(grid[n[0]][n[1] : current[1]])

            n_score = score + cost
            if n_score < scores[n]:
                scores[n] = n_score
                unsolved.put((n_score, n))

    raise ValueError("No path through the grid.")


def part1(data: str = DATA) -> int:
    """Solve Part 1.

    :param data: The input data.
    :returns: The solution.
    """
    grid = parse_input(data)
    return a_star(grid, 1, 3)


def part2(data: str = DATA) -> int:
    """Solve Part 2.

    :param data: The input data.
    :returns: The solution.
    """
    grid = parse_input(data)
    return a_star(grid, 4, 10)
