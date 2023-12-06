"""Advent of Code 2015 - Day 6

Day 6: Probably a Fire Hazard
=============================

Because your neighbors keep defeating you in the holiday house decorating
contest year after year, you've decided to deploy one million lights in a
1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed
you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at
each corner are at `0,0`, `0,999`, `999,999`, and `999,0`. The instructions
include whether to `turn on`, `turn off`, or toggle various inclusive ranges
given as coordinate pairs. Each coordinate pair represents opposite corners of
a rectangle, inclusive; a coordinate pair like `0,0 through 2,2` therefore
refers to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by
doing the instructions Santa sent you in order.

For example:

- `turn on 0,0 through 999,999` would turn on (or leave on) every light.
- `toggle 0,0 through 999,0` would toggle the first line of 1000 lights,
    turning off the ones that were on, and turning on the ones that were off.
- `turn off 499,499 through 500,500` would turn off (or leave off) the middle
    four lights.

After following the instructions, how many lights are lit?

Part Two
========

You just finish implementing your winning light pattern when you realize you
mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each
light can have a brightness of zero or more. The lights all start at zero.

- The phrase `turn on` actually means that you should increase the brightness
    of those lights by `1`.

- The phrase `turn off` actually means that you should decrease the brightness
    of those lights by `1`, to a minimum of zero.

- The phrase `toggle` actually means that you should increase the brightness of
    those lights by `2`.

What is the total brightness of all lights combined after following Santa's
instructions?

For example:

- `turn on 0,0 through 0,0` would increase the total brightness by `1`.
- `toggle 0,0 through 999,999` would increase the total brightness by `2000000`.
"""

import re
from typing import List, Tuple

from aocd import get_data

DATA = get_data(year=2015, day=6)


def parse_instruction(instruction: str) -> Tuple[str, Tuple[int, int], Tuple[int, int]]:
    """Parse the instruction string.

    :param instruction: The instruction text.
    :returns: A tuple of `(command, corner1, corner2)`, with `command` being
        the command to take effect and `corner1` and `corner2` as tuples of
        x,y coordinates.
    """
    instruction_re = r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)"
    if match := re.match(instruction_re, instruction.strip()):
        command, x0, y0, x1, y1 = (
            match.group(1),
            int(match.group(2)),
            int(match.group(3)),
            int(match.group(4)),
            int(match.group(5)),
        )
        return command, (x0, y0), (x1, y1)

    raise ValueError("No instruction")


def create_lights() -> List[List[int]]:
    """Create a light field."""
    lights = []
    for _ in range(1000):
        lights.append([0] * 1000)

    return lights


def part1(data: str = DATA) -> int:
    """Calculate part 1.

    :param data: The input data.
    :returns: The number of lights that are lit.
    """
    lights = create_lights()
    for instruction in data.splitlines():
        try:
            command, corner1, corner2 = parse_instruction(instruction)
        except ValueError:
            continue

        for i in range(corner1[0], corner2[0] + 1):
            for j in range(corner1[1], corner2[1] + 1):
                if command == "turn on":
                    lights[i][j] = 1
                elif command == "turn off":
                    lights[i][j] = 0
                elif command == "toggle":
                    lights[i][j] ^= 1

    return sum(sum(row) for row in lights)


def part2(data: str = DATA) -> int:
    """Calculate part 2.

    :param data: The input data.
    :returns: Thr total brightness.
    """
    lights = create_lights()
    for instruction in data.splitlines():
        command, corner1, corner2 = parse_instruction(instruction)
        for i in range(corner1[0], corner2[0] + 1):
            for j in range(corner1[1], corner2[1] + 1):
                if command == "turn on":
                    lights[i][j] += 1
                elif command == "turn off":
                    lights[i][j] = max(lights[i][j] - 1, 0)
                elif command == "toggle":
                    lights[i][j] += 2

    return sum(sum(row) for row in lights)
