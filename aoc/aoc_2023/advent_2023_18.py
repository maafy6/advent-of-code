"""Advent of Code 2023: Day 18

Day 18: Lavaduct Lagoon
=======================

Thanks to your efforts, the machine parts factory is one of the first factories
up and running since the lavafall came back. However, to catch up with the large
backlog of parts requests, the factory will also need a large supply of lava for
a while; the Elves have already started creating a large lagoon nearby for this
purpose.

However, they aren't sure the lagoon will be big enough; they've asked you to
take a look at the dig plan (your puzzle input). For example:

```
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
```
The digger starts in a 1 meter cube hole in the ground. They then dig the
specified number of meters up (`U`), down (`D`), left (`L`), or right (`R`),
clearing full 1 meter cubes as they go. The directions are given as seen from
above, so if "up" were north, then "right" would be east, and so on. Each trench
is also listed with the color that the edge of the trench should be painted as
an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following
loop of trench (`#`) having been dug out from otherwise ground-level terrain
(`.`):

```
#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######
```
At this point, the trench could contain 38 cubic meters of lava. However, this
is just the edge of the lagoon; the next step is to dig out the interior so that
it is one meter deep as well:

```
#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######
```
Now, the lagoon can contain a much more respectable `62` cubic meters of lava.
While the interior is dug out, the edges are also painted according to the color
codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their
dig plan, how many cubic meters of lava could it hold?
"""

import re
from collections import defaultdict
from typing import Literal, Self

from aocd import get_data

from .advent_2023_10 import get_contained_tiles, get_loop_tiles
from .advent_2023_10 import parse_data as read_pipe_map

DATA = get_data(year=2023, day=18)


Direction = Literal["L", "R", "D", "U"]
Point = tuple[int, int]


class Polygon:
    """Polygon model."""

    def __init__(self) -> None:
        """Initialize the polygon."""
        self._points: list[Point] = [(0, 0)]
        self._lines: list[tuple[Point, Point]] = []
        self._bounds: dict[Direction, int] = {k: 0 for k in "LRDU"}
        self._h_lines: list[tuple[Point, Point]] = []
        self._v_lines: list[tuple[Point, Point]] = []

    def count(self) -> int:
        """Return the number of tiles included in the polygon, including border tiles."""
        pipe_map = read_pipe_map(self.to_pipe_map())
        return len(get_contained_tiles(pipe_map)) + len(get_loop_tiles(pipe_map))

    def to_pipe_map(self) -> str:
        """Generate a pipe map string from the polygon.

        c.f. AOC 2023-10 for where the pipe map came from.

        :returns: The pipe map string.
        """
        h_shift = -self._bounds["L"]
        v_shift = -self._bounds["U"]

        points = [(x + h_shift, y + v_shift) for (x, y) in self._points]

        grid_map = defaultdict(lambda: defaultdict(lambda: "."))
        last_point = None
        for point in points:
            x, y = point
            if last_point is None:
                grid_map[y][x] = "S"
            else:
                x0, y0 = last_point
                if x == x0:
                    if grid_map[y][x] != "S":
                        grid_map[y][x] = "v" if y > y0 else "^"

                    if grid_map[y0][x0] == ">":
                        grid_map[y0][x0] = "7" if y > y0 else "J"
                    elif grid_map[y0][x0] == "<":
                        grid_map[y0][x0] = "F" if y > y0 else "L"

                    for i in range(min(y0, y) + 1, max(y0, y)):
                        grid_map[i][x] = "|"

                elif y == y0:
                    if grid_map[y][x] != "S":
                        grid_map[y][x] = ">" if x > x0 else "<"

                    if grid_map[y0][x0] == "^":
                        grid_map[y0][x0] = "F" if x > x0 else "7"
                    elif grid_map[y0][x0] == "v":
                        grid_map[y0][x0] = "L" if x > x0 else "J"

                    for i in range(min(x0, x) + 1, max(x0, x)):
                        grid_map[y][i] = "-"

            last_point = point

        return "\n".join(
            "".join(grid_map[i][j] for j in range(self._bounds["R"] + h_shift + 1))
            for i in range(self._bounds["D"] + v_shift + 1)
        )

    def _add_point(self, direction: Direction, count: int) -> None:
        """Add a point to the polygon.

        :param direction: The direction to extend the polygon in.
        :param count: The number of units to extend the polygon in.
        """
        last_point = self._points[-1]

        if direction == "L":
            next_point = (last_point[0] - count, last_point[1])
            self._bounds["L"] = min(self._bounds["L"], next_point[0])
            self._h_lines.append((next_point, last_point))
        elif direction == "R":
            next_point = (last_point[0] + count, last_point[1])
            self._bounds["R"] = max(self._bounds["R"], next_point[0])
            self._h_lines.append((last_point, next_point))
        elif direction == "D":
            next_point = (last_point[0], last_point[1] + count)
            self._bounds["D"] = max(self._bounds["D"], next_point[1])
            self._v_lines.append((last_point, next_point))
        elif direction == "U":
            next_point = (last_point[0], last_point[1] - count)
            self._bounds["U"] = min(self._bounds["U"], next_point[1])
            self._v_lines.append((next_point, last_point))

        self._points.append(next_point)
        self._lines.append((last_point, next_point))

    @classmethod
    def loads(cls, data: str) -> Self:
        """Load a polygon from the string.

        :param data: The data describing the polygon.
        :returns: The parsed polygon.
        """
        poly = cls()
        for line in data.splitlines():
            if match := re.match(r"([LRDU])\s+(\d+)\s+\(#[0-9a-f]{6}\)", line):
                direction, count = match.groups()
                poly._add_point(direction, int(count))

        if len(poly._points) < 4 or poly._points[0] != poly._points[-1]:
            raise ValueError("Polygon is not closed.")

        return poly


def part1(data: str = DATA) -> int:
    """Solve Part 1.

    :param data: The input data.
    :returns: The solution.
    """

    poly = Polygon.loads(data, part=1)
    return poly.count()


def part2(data: str = DATA) -> int:
    """Solve Part 2.

    :param data: The input data.
    :returns: The solution.
    """
