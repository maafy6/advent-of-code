"""Advent of Code 2023: Day 14

Day 14: Parabolic Reflector Dish
================================

You reach the place where all of the mirrors were pointing: a massive parabolic
reflector dish attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are
roughly in the shape of a parabolic reflector dish, each individual mirror seems
to be pointing in slightly the wrong direction. If the dish is meant to focus
light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the
reflector dish, maybe you can go where it's pointing and use the light to fix
the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via
an elaborate system of ropes and pulleys to a large metal platform below the
dish. The platform is covered in large rocks of various shapes. Depending on
their position, the weight of the rocks deforms the platform, and the shape of
the platform controls which ropes move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a
control panel on the side that lets you tilt it in one of four directions! The
rounded rocks (`O`) will roll when the platform is tilted, while the cube-shaped
rocks (`#`) will stay in place. You note the positions of all of the empty
spaces (`.`) and rocks (your puzzle input). For example:

```
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
```

Start by tilting the lever so all of the rocks will slide north as far as they
will go:

```
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
```

You notice that the support beams along the north side of the platform are
damaged; to ensure the platform doesn't collapse, you should calculate the total
load on the north support beams.

The amount of load caused by a single rounded rock (`O`) is equal to the number
of rows from the rock to the south edge of the platform, including the row the
rock is on. (Cube-shaped rocks (`#`) don't contribute to load.) So, the amount
of load caused by each rock in each row is as follows:

```
OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1
```

The total load is the sum of the load caused by all of the rounded rocks. In
this example, the total load is `136`.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is
the total load on the north support beams?

Part Two
========

The parabolic reflector dish deforms, but not in a way that focuses the beam. To
do that, you'll need to move the rocks to the edges of the platform.
Fortunately, a button on the side of the control panel labeled "spin cycle"
attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north,
then west, then south, then east. After each tilt, the rounded rocks roll as far
as they can before the platform tilts in the next direction. After one cycle,
the platform will have finished rolling the rounded rocks in those four
directions in that order.

Here's what happens in the example above after each of the first few cycles:

```
After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
```

This process should work if you leave it running long enough, but you're still
worried about the north support beams. To make sure they'll survive for a while,
you need to calculate the total load on the north support beams after
`1000000000` cycles.

In the above example, after `1000000000` cycles, the total load on the north
support beams is `64`.

Run the spin cycle for `1000000000` cycles. Afterward, what is the total load on
the north support beams?
"""

from collections.abc import Iterator

from aocd import get_data

DATA = get_data(year=2023, day=14)

PlatformGrid = tuple[str]


def group_str(string: str) -> Iterator[str]:
    """Slightly Optimized replacement for `itertools.groupby` for `str`.

    ```
    list(group_by("..#.OOO##..")) == ["..", "#", ".", "OOO", "##", ".."]
    ```

    :param string: The string to group.
    :yields: Successive strings of the same character.
    """
    current = ""
    for c in string:
        if not current:
            current = c
            continue

        if c == current[0]:
            current += c
        else:
            yield current
            current = c

    if current:
        yield current


def parse_input(data: str) -> PlatformGrid:
    """Parse the input data.

    :param data: The input data.
    :returns: The parsed platform data.
    """
    return tuple(data.splitlines())


def rotate(platform: PlatformGrid) -> PlatformGrid:
    """Rotate the platform 90 degrees clockwise.

    1N2    4W1
    WCE -> SCN
    4S3    3E2

    :param platform: The platform.
    :returns: The rotated platform.
    """
    return tuple(
        "".join(row[i] for row in reversed(platform)) for i in range(len(platform[0]))
    )


def tilt_platform(platform: PlatformGrid) -> PlatformGrid:
    """Tilt the platform to move rocks as far as possible to the edge.

    :param platform: Tilt the platform in the E direction.
    :returns: The tilted platform.
    """
    rotated = rotate(platform)
    tilted = []
    for row in rotated:
        tilted_row = ""
        total_count, round_count = 0, 0

        for grp in group_str(row):
            if grp[0] == "O":
                count = len(grp)
                total_count += count
                round_count += count
            elif grp[0] == "#":
                if total_count:
                    tilted_row += "." * (total_count - round_count)
                    tilted_row += "O" * round_count
                tilted_row += grp
                total_count, round_count = 0, 0
            elif grp[0] == ".":
                total_count += len(grp)

        tilted_row += "." * (total_count - round_count)
        tilted_row += "O" * round_count
        tilted.append(tilted_row)

    return tuple(t for t in tilted)


def tilt_cycle(platform: PlatformGrid) -> PlatformGrid:
    """Run a tilt cycle on the platform, tilting it to the north, west, south,
        and east (in that order.)

    :param platform: The platform.
    :returns: The platform tilted across all cardinal directions.
    """
    for _ in range(4):
        platform = tilt_platform(platform)

    return platform


def calculate_load(platform: PlatformGrid) -> int:
    """Calculate the load on the north platform wall.

    :param platform: The platform.
    :returns: The calculated load.
    """
    return sum(
        0 if row[i] in ".#" else i + 1 for row in platform for i in range(len(row))
    )


def part1(data: str = DATA) -> int:
    """Solve Part 1.

    :param data: The input data.
    :returns: The solution.
    """
    platform = parse_input(data)
    platform = tilt_platform(platform)
    return calculate_load(platform)


def part2(data: str = DATA) -> int:
    """Solve Part 2.

    :param data: The input data.
    :returns: The solution.
    """
    iterations = 1000000000
    platform = parse_input(data)

    platforms = []
    for _ in range(iterations):
        if (platform := tilt_cycle(platform)) in platforms:
            break

        platforms.append(platform)

    loop_start = platforms.index(platform)
    loop_length = len(platforms) - loop_start

    offset = loop_start + (iterations - loop_start - 1) % loop_length

    # Rotate the platform one last time to calculate the offset.
    return calculate_load(rotate(platforms[offset]))
