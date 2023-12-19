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

Part Two
========

The Elves were right to be concerned; the planned lagoon would be much too
small.

After a few minutes, someone realizes what happened; someone swapped the color
and instruction parameters when producing the dig plan. They don't have time to
fix the bug; one of them asks if you can extract the correct instructions from
the hexadecimal codes.

Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal
digits encode the distance in meters as a five-digit hexadecimal number. The
last hexadecimal digit encodes the direction to dig: `0` means `R`, `1` means
`D`, `2` means `L`, and `3` means `U`.

So, in the above example, the hexadecimal codes can be converted into the true
instructions:

- `#70c710` = `R 461937`
- `#0dc571` = `D 56407`
- `#5713f0` = `R 356671`
- `#d2c081` = `D 863240`
- `#59c680` = `R 367720`
- `#411b91` = `D 266681`
- `#8ceee2` = `L 577262`
- `#caa173` = `U 829975`
- `#1b58a2` = `L 112010`
- `#caa171` = `D 829975`
- `#7807d2` = `L 491645`
- `#a77fa3` = `U 686074`
- `#015232` = `L 5411`
- `#7a21e3` = `U 500254`

Digging out this loop and its interior produces a lagoon that can hold an
impressive `952408144115` cubic meters of lava.

Convert the hexadecimal color codes into the correct instructions; if the Elves
follow this new dig plan, how many cubic meters of lava could the lagoon hold?
"""

import re
from typing import Literal, Self

from aocd import get_data

DATA = get_data(year=2023, day=18)


Direction = Literal["L", "R", "D", "U"]
Point = tuple[int, int]


class Polygon:
    """Polygon model."""

    def __init__(self) -> None:
        """Initialize the polygon."""
        self._points: list[Point] = [(0, 0)]
        self._h_lines: list[tuple[Point, Point]] = []

    def count(self) -> int:
        """Return the number of tiles included in the polygon, including border tiles."""
        current = []
        last_y = None
        area = 0

        # Scan the horizontal lines of polygon. Maintain an initially empty
        # list of active horizontal ranges that mark a square as being in the
        # polygon. Each time a new horizontal line is encountered, calculate
        # the area of the squares in the ranges since the last horizontal line
        # and update the ranges.
        for p0, p1 in sorted(self._h_lines, key=lambda l: (l[0][1], l[0][0])):
            h_range = range(p0[0], p1[0] + 1)
            if last_y is None:
                current = [h_range]
                last_y = p0[1]
                continue

            # Add in the area of the ranges from this horizontal line to the
            # previous. `p0[1] - last_y` gives the height, while the sum over
            # all the ranges gives the total width.
            area += (p0[1] - last_y) * sum((r.stop - r.start) for r in current)
            last_y = p0[1]

            # Rebuild the list of horizontal ranges. If there the new horizontal
            # lines causes squares below it to no longer be in the polygon,
            # then the area of those border squares should be added in here.
            updated_ranges: list[range] = []
            merged = False
            for r in current:
                # (1) The new horizontal line matches the existing range exactly.
                #
                #       #######
                #       ~~~~~~~
                #
                #   In this case, we add in the area for the border ~ squares
                #   and remove the range from the list by not adding it back in
                #   to `updated_ranges`.
                if h_range.start == r.start and h_range.stop == r.stop:
                    area += h_range.stop - h_range.start
                    merged = True
                # (2) The new horizontal line is entirely enclosed in the range.
                #
                #       #######
                #         ~~~
                #
                #   Split the existing range into two ranges:
                #
                #       ### ###
                #
                #   Note that the endpoints of the considered range need to be
                #   present in the new ranges.
                elif r.start < h_range.start and h_range.stop < r.stop:
                    updated_ranges.append(range(r.start, h_range.start + 1))
                    updated_ranges.append(range(h_range.stop - 1, r.stop))
                    merged = True
                    area += h_range.stop - h_range.start - 2
                # (3) The new horizontal line starts where the range stops:
                #
                #       #######
                #             ~~~~
                #
                #   Extend the range to cover the combined effect.
                #
                #       ##########
                elif h_range.start + 1 == r.stop:
                    merged = True
                    updated_ranges.append(range(r.start, h_range.stop))
                # (3b) Special case where a new horizontal line "joins" two
                #   existing ranges.
                #
                #       #######  ####
                #             ~~~~
                #
                #   To detect this case, look back at the last entry in the
                #   updated ranges and see if the previous one now touches this
                #   one. This requires us to keep the range list sorted by
                #   start point.
                #
                #       #############
                elif updated_ranges and updated_ranges[-1].stop == r.start + 1:
                    left_range = updated_ranges.pop()
                    updated_ranges.append(range(left_range.start, r.stop))
                # (4) The new horizontal line stops where the range starts:
                #
                #          #######
                #       ~~~~
                #
                #   Extend the range to cover the combined effect.
                #
                #       ##########
                elif h_range.stop == r.start + 1:
                    merged = True
                    updated_ranges.append(range(h_range.start, r.stop))
                # (5) The new horizontal line and range have the same start point:
                #
                #       #######
                #       ~~~~
                #
                #   Contract the range, ensuring the internal endpoint stays in
                #   the polygon.
                #
                #          ####
                elif h_range.start == r.start:
                    updated_ranges.append(range(h_range.stop - 1, r.stop))
                    merged = True
                    area += h_range.stop - h_range.start - 1
                # (6) The new horizontal line and range have the same start point:
                #
                #       #######
                #          ~~~~
                #
                #   Contract the range, ensuring the internal endpoint stays in
                #   the polygon.
                #
                #       ####
                elif h_range.stop == r.stop:
                    merged = True
                    updated_ranges.append(range(r.start, h_range.start + 1))
                    area += h_range.stop - h_range.start - 1
                # (7) The new line is completely outside of this range, so it
                #   should be carried over unchanged.
                else:
                    updated_ranges.append(r)

            if not merged:
                updated_ranges.append(h_range)

            current = sorted(updated_ranges, key=lambda r: r.start)

        return area

    def _add_point(self, direction: Direction, count: int) -> None:
        """Add a point to the polygon.

        :param direction: The direction to extend the polygon in.
        :param count: The number of units to extend the polygon in.
        """
        last_point = self._points[-1]

        if direction == "L":
            next_point = (last_point[0] - count, last_point[1])
            self._h_lines.append((next_point, last_point))
        elif direction == "R":
            next_point = (last_point[0] + count, last_point[1])
            self._h_lines.append((last_point, next_point))
        elif direction == "D":
            next_point = (last_point[0], last_point[1] + count)
        elif direction == "U":
            next_point = (last_point[0], last_point[1] - count)

        self._points.append(next_point)

    @classmethod
    def loads(cls, data: str, *, part: int) -> Self:
        """Load a polygon from the string.

        :param data: The data describing the polygon.
        :returns: The parsed polygon.
        """
        poly = cls()
        for line in data.splitlines():
            if part == 1:
                if match := re.match(r"([LRDU])\s+(\d+)\s+\(#[0-9a-f]{6}\)", line):
                    direction, count_str = match.groups()
                    count = int(count_str)
                else:
                    raise ValueError("Invalid line.")
            if part == 2:
                if match := re.match(
                    r"[LRDU]\s+\d+\s+\(#([0-9a-f]{5})([0123])\)", line
                ):
                    count_str, dir_str = match.groups()
                    count = int(count_str, base=16)
                    direction = {"0": "R", "1": "D", "2": "L", "3": "U"}[dir_str]
                else:
                    raise ValueError("Invalid line.")

            poly._add_point(direction, count)

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
    poly = Polygon.loads(data, part=2)
    return poly.count()
