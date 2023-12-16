r"""Advent of Code 2023: Day 16

Day 16: The Floor Will Be Lava
==============================

With the beam of light completely focused somewhere, the reindeer leads you
deeper still into the Lava Production Facility. At some point, you realize that
the steel facility walls have been replaced with cave, and the doorways are just
cave, and the floor is cave, and you're pretty sure this is actually just a
giant cave.

Finally, as you approach what must be the heart of the mountain, you see a
bright light in a cavern up ahead. There, you discover that the beam of light
you so carefully focused is emerging from the cavern wall closest to the
facility and pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional
square grid containing empty space (`.`), mirrors (`/` and `\`), and splitters
(`|` and `-`).

The contraption is aligned so that most of the beam bounces around the grid, but
each tile on the grid converts some of the beam's light into heat to melt the
rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

```
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
```

The beam enters in the top-left corner from the left and heading to the right.
Then, its behavior depends on what it encounters as it moves:

- If the beam encounters empty space (`.`), it continues in the same direction.
- If the beam encounters a mirror (`/` or `\`), the beam is reflected 90 degrees
    depending on the angle of the mirror. For instance, a rightward-moving beam
    that encounters a `/` mirror would continue upward in the mirror's column,
    while a rightward-moving beam that encounters a `\` mirror would continue
    downward from the mirror's column.
- If the beam encounters the pointy end of a splitter (`|` or `-`), the beam
    passes through the splitter as if the splitter were empty space. For
    instance, a rightward-moving beam that encounters a `-` splitter would
    continue in the same direction.
- If the beam encounters the flat side of a splitter (`|` or `-`), the beam is
    split into two beams going in each of the two directions the splitter's
    pointy ends are pointing. For instance, a rightward-moving beam that
    encounters a `|` splitter would split into two beams: one that continues
    upward from the splitter's column and one that continues downward from the
    splitter's column.

Beams do not interact with other beams; a tile can have many beams passing
through it at the same time. A tile is energized if that tile has at least one
beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the
contraption:

```
>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
```

Beams are only shown on empty tiles; arrows indicate the direction of the beams.
If a tile contains beams moving in multiple directions, the number of distinct
directions is shown instead. Here is the same diagram but instead only showing
whether a tile is energized (`#`) or not (`.`):

```
######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
```

Ultimately, in this example, `46` tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the
contraption, you need to start by analyzing the current situation. With the beam
starting in the top-left heading right, how many tiles end up being energized?

Part Two
========

As you try to work out what might be wrong, the reindeer tugs on your shirt and
leads you to a nearby control panel. There, a collection of buttons lets you
align the contraption so that the beam enters from any edge tile and heading
away from that edge. (You can choose either of two directions for the beam if it
starts on a corner; for instance, if the beam starts in the bottom-right corner,
it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile
in the bottom row (heading upward), any tile in the leftmost column (heading
right), or any tile in the rightmost column (heading left). To produce lava, you
need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth
tile from the left in the top row:

```
.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..
```

Using this configuration, `51` tiles are energized:

```
.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..
```

Find the initial beam configuration that energizes the largest number of tiles;
how many tiles are energized in that configuration?
"""

import functools
from multiprocessing import Pool, cpu_count
from typing import Literal

from aocd import get_data

DATA = get_data(year=2023, day=16)


DirectionStr = Literal[">", "<", "^", "v"]
Beam = tuple[int, int, DirectionStr]


def parse_input(data: str) -> tuple[str]:
    """Parse the input.

    :param data: The input data.
    :returns: A tuple of lines.
    """
    return tuple(data.splitlines())


def next_square(  # pylint: disable=too-many-branches,too-many-statements
    grid: tuple[str], beam: Beam
) -> list[Beam]:
    """Given a beam at a square in the grid, return the next beams.

    :param grid: The grid map.
    :param beam: The current beam position and direction.
    :returns: A list of beams after this beam passes through the given
        position.
    """
    x, y, direction = beam
    tile = grid[y][x]

    beams = []

    if tile == ".":
        if direction == ">" and x + 1 < len(grid[y]):
            beams.append((x + 1, y, direction))
        elif direction == "<" and x > 0:
            beams.append((x - 1, y, direction))
        elif direction == "^" and y > 0:
            beams.append((x, y - 1, direction))
        elif direction == "v" and y + 1 < len(grid):
            beams.append((x, y + 1, direction))

    elif tile == "/":
        if direction == ">" and y > 0:
            beams.append((x, y - 1, "^"))
        elif direction == "<" and y + 1 < len(grid):
            beams.append((x, y + 1, "v"))
        elif direction == "^" and x + 1 < len(grid[y]):
            beams.append((x + 1, y, ">"))
        elif direction == "v" and x > 0:
            beams.append((x - 1, y, "<"))

    elif tile == "\\":
        if direction == ">" and y + 1 < len(grid):
            beams.append((x, y + 1, "v"))
        elif direction == "<" and y > 0:
            beams.append((x, y - 1, "^"))
        elif direction == "^" and x > 0:
            beams.append((x - 1, y, "<"))
        elif direction == "v" and x + 1 < len(grid[y]):
            beams.append((x + 1, y, ">"))

    elif tile == "-":
        if direction == ">" and x + 1 < len(grid[y]):
            beams.append((x + 1, y, direction))
        elif direction == "<" and x > 0:
            beams.append((x - 1, y, direction))
        elif direction in "^v":
            if x > 0:
                beams.append((x - 1, y, "<"))
            if x + 1 < len(grid[y]):
                beams.append((x + 1, y, ">"))

    if tile == "|":
        if direction in "><":
            if y > 0:
                beams.append((x, y - 1, "^"))
            if y + 1 < len(grid):
                beams.append((x, y + 1, "v"))
        elif direction == "^" and y > 0:
            beams.append((x, y - 1, direction))
        elif direction == "v" and y + 1 < len(grid):
            beams.append((x, y + 1, direction))

    return beams


def illuminate(grid: tuple[str], beam: Beam = (0, 0, ">")) -> int:
    """Return the number of squares illuminated by the starting beam.

    :param grid: The grid map.
    :param beam: The initial beam.
    :returns: The number of squares illuminated.
    """
    seen = set()
    beams = [beam]
    while beams:
        next_beam = beams.pop()
        seen.add(next_beam)
        next_beams = next_square(grid, next_beam)
        beams += [b for b in next_beams if b not in seen]

    return len(set((x, y) for x, y, _ in seen))


def part1(data: str = DATA) -> int:
    """Solve Part 1.

    :param data: The input data.
    :returns: The solution.
    """
    return illuminate(parse_input(data))


def part2(data: str = DATA) -> int:
    """Solve Part 2.

    :param data: The input data.
    :returns: The solution.
    """
    grid = parse_input(data)
    grid_size = len(grid[0]), len(grid)

    starting_beams = []
    starting_beams += [(x, 0, "v") for x in range(grid_size[0])]
    starting_beams += [(x, grid_size[1] - 1, "^") for x in range(grid_size[0])]
    starting_beams += [(0, y, ">") for y in range(grid_size[1])]
    starting_beams += [(grid_size[0] - 1, y, "<") for y in range(grid_size[1])]

    with Pool(cpu_count()) as pool:
        illum_func = functools.partial(illuminate, grid)
        illuminated = pool.map(illum_func, starting_beams)

    return max(illuminated)
