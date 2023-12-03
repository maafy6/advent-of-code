"""Advent of Code 2023 - Day 3

Day 3: Gear Ratios
==================

You and the Elf eventually reach a gondola lift station; he says the gondola
lift will take you up to the water source, but this is as far as he can bring
you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem:
they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of
surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working
right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine,
but nobody can figure out which one. If you can add up all the part numbers in
the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of
the engine. There are lots of numbers and symbols you don't really understand,
but apparently any number adjacent to a symbol, even diagonally, is a "part
number" and should be included in your sum. (Periods (`.`) do not count as a
symbol.)

Here is an example engine schematic:

```
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
```

In this schematic, two numbers are not part numbers because they are not
adjacent to a symbol: `114` (top right) and `58` (middle right). Every other
number is adjacent to a symbol and so is a part number; their sum is `4361`.

Of course, the actual engine schematic is much larger. What is the sum of all
of the part numbers in the engine schematic?

Part Two
========

The engineer finds the missing part and installs it in the engine! As the
engine springs to life, you jump in the closest gondola, finally ready to
ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong?
Fortunately, the gondola has a phone labeled "help", so you pick it up and the
engineer answers.

Before you can explain the situation, she suggests that you look out the
window. There stands the engineer, holding a phone in one hand and waving with
the other. You're going so slowly that you haven't even left the station. You
exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is
wrong. A gear is any `*` symbol that is adjacent to exactly two part numbers.
Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so
that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

```
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
```

In this schematic, there are two gears. The first is in the top left; it has
part numbers `467` and `35`, so its gear ratio is 16345. The second gear is in
the lower right; its gear ratio is `451490`. (The * adjacent to 617 is not a
gear because it is only adjacent to one part number.) Adding up all of the gear
ratios produces `467835`.

What is the sum of all of the gear ratios in your engine schematic?
"""

import re
from copy import copy
from typing import Iterator, Sequence

from aocd import get_data

DATA = get_data(year=2023, day=3)


def part_numbers(schematic: str) -> Sequence[int]:
    """Get the part numbers listed in the schematic.

    :param schematic: The schematic.
    :returns: A list of part numbers found in the schematic.
    """
    line_length = schematic.index("\n") + 1

    number_matches = []
    for number in re.finditer(r"(\d+)", schematic):
        x = (number.span()[0] % line_length, number.span()[1] % line_length)
        y = number.span()[0] // line_length
        val = int(number.group(0))
        number_matches.append((val, x, y))

    part_nums = []
    for part in re.finditer(r"([^\.0-9\n])", schematic):
        x = part.span()[0] % line_length
        y = part.span()[0] // line_length

        for number in copy(number_matches):
            val, num_x, num_y = number
            if not y - 1 <= num_y <= y + 1:
                continue

            if num_x[1] < x or x < num_x[0] - 1:
                continue

            part_nums.append(val)
            number_matches.remove(number)

    return part_nums


def part1(data: str = DATA) -> int:
    """Solve part 1.

    :param data: The input data.
    :returns: The sum of all part numbers.
    """
    return sum(part_numbers(data))


def gen_gear_ratios(schematic: str) -> Iterator[int]:
    """Yield the gear ratios for the gears in the schematic.

    :param schematic: The schematic.
    :yields: The gear ratios for the gears in the schematic.
    """

    line_length = schematic.index("\n") + 1

    number_matches = []
    for number in re.finditer(r"(\d+)", schematic):
        x = (number.span()[0] % line_length, number.span()[1] % line_length)
        y = number.span()[0] // line_length
        val = int(number.group(0))
        number_matches.append((val, x, y))

    for part in re.finditer(r"([\*])", schematic):
        x = part.span()[0] % line_length
        y = part.span()[0] // line_length

        part_nums = []
        for number in number_matches:
            val, num_x, num_y = number
            if not y - 1 <= num_y <= y + 1:
                continue

            if num_x[1] < x or x < num_x[0] - 1:
                continue

            part_nums.append(val)

        if len(part_nums) == 2:
            yield part_nums[0] * part_nums[1]


def part2(data: str = DATA) -> int:
    """Solve part 2.

    :param data: The input data.
    :returns: The sum of all gear ratios.
    """
    return sum(gen_gear_ratios(data))
