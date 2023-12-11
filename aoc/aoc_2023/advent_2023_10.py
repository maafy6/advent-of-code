"""Advent of Code 2023: Day 10

Day 10: Pipe Maze
=================

You use the hang glider to ride the hot air from Desert Island all the way up to
the floating metal island. This island is surprisingly cold and there definitely
aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals.
However, you do occasionally find signposts labeled "Hot Springs" pointing in a
seemingly consistent direction; maybe you can find someone at the hot springs
and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As
you stop to admire some metal grass, you notice something metallic scurry away
in your peripheral vision and jump into a big pipe! It didn't look like any
animal you've ever seen; if you want a better look, you'll need to get ahead of
it.

Scanning the area, you discover that the entire field you're standing on is
densely packed with pipes; it was hard to tell at first because they're the same
metallic silver color as the "ground". You make a quick sketch of all of the
surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

- `|` is a vertical pipe connecting north and south.
- `-` is a horizontal pipe connecting east and west.
- `L` is a 90-degree bend connecting north and east.
- `J` is a 90-degree bend connecting north and west.
- `7` is a 90-degree bend connecting south and west.
- `F` is a 90-degree bend connecting south and east.
- `.` is ground; there is no pipe in this tile.
- `S` is the starting position of the animal; there is a pipe on this tile, but
    your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that
contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

```
.....
.F-7.
.|.|.
.L-J.
.....
```

If the animal had entered this loop in the northwest corner, the sketch would
instead look like this:

```
.....
.S-7.
.|.|.
.L-J.
.....
```

In the above diagram, the `S` tile is still a 90-degree `F` bend: you can tell
because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This
sketch shows the same loop as above:

```
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
```

In the above diagram, you can still figure out which pipes form the main loop:
they're the ones connected to `S`, pipes those pipes connect to, pipes those
pipes connect to, and so on. Every pipe in the main loop connects to its two
neighbors (including `S`, which will have exactly two pipes connecting to it,
and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

```
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
```

Here's the same example sketch with the extra, non-main-loop pipe tiles also
shown:

```
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
```

If you want to get out ahead of the animal, you should find the tile in the loop
that is farthest from the starting position. Because the animal is in the pipe,
it doesn't make sense to measure this by direct distance. Instead, you need to
find the tile that would take the longest number of steps along the loop to
reach from the starting point - regardless of which way around the loop the
animal went.

In the first example with the square loop:

```
.....
.S-7.
.|.|.
.L-J.
.....
```

You can count the distance each tile in the loop is from the starting point like
this:

```
.....
.012.
.1.3.
.234.
.....
```

In this example, the farthest point from the start is `4` steps away.

Here's the more complex loop again:

```
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
```

Here are the distances for each tile on that loop:

```
..45.
.236.
01.78
14567
23...
```

Find the single giant loop starting at `S`. How many steps along the loop does
it take to get from the starting position to the point farthest from the
starting position?

Part Two
========

You quickly reach the farthest point of the loop, but the animal never emerges.
Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest,
you should calculate how many tiles are contained within the loop. For example:

```
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
```

The above loop encloses merely four tiles - the two pairs of `.` in the
southwest and southeast (marked `I` below). The middle `.` tiles (marked `O`
below) are not in the loop. Here is the same loop again with those regions
marked:

```
...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
```

In fact, there doesn't even need to be a full tile path to the outside for tiles
to count as outside the loop - squeezing between pipes is also allowed! Here,
`I` is still within the loop and `O` is still outside the loop:

```
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
```

In both of the above examples, `4` tiles are enclosed by the loop.

Here's a larger example:

```
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
```

The above sketch has many random bits of ground, some of which are in the loop
(`I`) and some of which are outside it (`O`):

```
OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
```

In this larger example, `8` tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the
loop. Here's another example with many bits of junk pipe lying around that
aren't connected to the main loop at all:

```
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
```

Here are just the tiles that are enclosed by the loop marked with `I`:

```
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
```

In this last example, `10` tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area
within the loop. How many tiles are enclosed by the loop?
"""

from copy import copy
from typing import Iterable

from aocd import get_data

DATA = get_data(year=2023, day=10)


def parse_data(data: str) -> list[list[str]]:
    """Parse the input data."""
    return [list(line) for line in data.splitlines()]


def get_connecting_neighbors(
    pipe_map: list[list[str]], pos: tuple[int, int]
) -> list[tuple[int, int]]:
    """Get the neighbors connected to the point at the given position.

    :param pipe_map: The pipe map.
    :param pos: The position of the point to get the connections for.
    :returns: The list of neighbors connected to the given position.
    """
    char = pipe_map[pos[0]][pos[1]]
    connected = []
    if char == "S":
        for i, j in [
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1),
        ]:
            if (
                0 <= i < len(pipe_map)
                and 0 <= j < len(pipe_map[pos[0]])
                and (pos[0], pos[1]) in get_connecting_neighbors(pipe_map, (i, j))
            ):
                connected.append((i, j))
    else:
        if char in "|LJ" and pos[0] > 0:
            connected.append((pos[0] - 1, pos[1]))
        if char in "|7F" and pos[0] < len(pipe_map):
            connected.append((pos[0] + 1, pos[1]))
        if char in "-J7" and pos[1] > 0:
            connected.append((pos[0], pos[1] - 1))
        if char in "-LF" and pos[1] < len(pipe_map[pos[0]]):
            connected.append((pos[0], pos[1] + 1))

    return connected


# functools.lrucache doesn't support list arguments, so we'll implement a poor
# man's version since it takes a couple seconds to run on large maps.
__get_loop_tiles_cache = {}


def get_loop_tiles(pipe_map: list[list[str]]) -> list[tuple[int, int]]:
    """Get a list of tiles in the loop started with "S".

    The returned loop tiles begins with the tile marked with "S" but are not
    in the order of traversal.

    :param pipe_map: The pipe map.
    :returns: A list of tiles on the loop marked with an "S".
    """
    map_hash = hash("\n".join("".join(l) for l in pipe_map))
    if map_hash in __get_loop_tiles_cache:
        return __get_loop_tiles_cache[map_hash]

    i, j = None, None
    for i, map_line in enumerate(pipe_map):
        if "S" in map_line:
            j = map_line.index("S")
            break

    if (i is None) or (j is None):
        raise ValueError("Starting point not found.")

    visited = [(i, j)]
    unchecked = [*get_connecting_neighbors(pipe_map, (i, j))]
    while unchecked:
        for p in copy(unchecked):
            for n in get_connecting_neighbors(pipe_map, p):
                if n not in visited:
                    visited.append(n)
                    unchecked.append(n)
            unchecked.remove(p)

    __get_loop_tiles_cache[map_hash] = visited
    return visited


def get_contained_tiles(pipe_map: Iterable[Iterable[str]]) -> list[tuple[int, int]]:
    """Get a list of points contained by the starting loop of the map.

    :param pipe_map: The pipe map.
    :returns: The list of contained tiles.
    """
    tiles = sorted(get_loop_tiles(pipe_map))

    contained = []
    for i, map_line in enumerate(pipe_map):
        for j in range(len(map_line)):
            if (i, j) in tiles:
                continue

            left = [p for p in tiles if p[0] == i and p[1] < j]

            enclosed = False
            last_corner = None
            for t in [pipe_map[l[0]][l[1]] for l in left]:
                if t == "|":
                    enclosed ^= True
                if t in "LJF7":
                    if t == "J":
                        enclosed ^= last_corner == "F"
                    elif t == "7":
                        enclosed ^= last_corner == "L"
                    last_corner = t

            if enclosed:
                pipe_map[i][j] = "I"
                contained.append((i, j))
            elif (i, j) not in tiles:
                pipe_map[i][j] = " "

    return contained


def part1(data: str = DATA) -> int:
    """Solve Part 1.

    :param data: The input data.
    :returns: The solution.
    """
    pipe_map = parse_data(data)
    tiles = get_loop_tiles(pipe_map)
    return len(tiles) // 2


def part2(data: str = DATA) -> int:
    """Solve Part 2.

    :param data: The input data.
    :returns: The solution.
    """
    pipe_map = parse_data(data)
    contained = get_contained_tiles(pipe_map)
    return len(contained)
