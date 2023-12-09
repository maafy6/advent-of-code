"""Advent of Code 2023: Day 8

Day 8: Haunted Wasteland
========================

You're still riding a camel across Desert Island when you spot a sandstorm
quickly approaching. When you turn to warn the Elf, she disappears before your
eyes! To be fair, she had just finished warning you about ghosts a few minutes
ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of
documents (your puzzle input) about how to navigate the desert. At least, you're
pretty sure that's what they are; one of the documents contains a list of
left/right instructions, and the rest of the documents seem to describe some
kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the
network. Perhaps if you have the camel follow the same instructions, you can
escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: `AAA` and `ZZZ`. You
feel like `AAA` is where you are now, and you have to follow the left/right
instructions until you reach `ZZZ`.

This format defines each node of the network individually. For example:

```
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
```

Starting with `AAA`, you need to look up the next element based on the next
left/right instruction in your input. In this example, start with `AAA` and go
right (`R`) by choosing the right element of `AAA`, `CCC`. Then, `L` means to
choose the left element of `CCC`, `ZZZ`. By following the left/right
instructions, you reach `ZZZ` in `2` steps.

Of course, you might not find `ZZZ` right away. If you run out of left/right
instructions, repeat the whole sequence of instructions as necessary: `RL`
really means `RLRLRLRLRLRLRLRL...` and so on. For example, here is a situation
that takes `6` steps to reach `ZZZ`:

```
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
```

Starting at `AAA`, follow the left/right instructions. How many steps are
required to reach ZZZ?

Part Two
========

The sandstorm is upon you and you aren't any closer to escaping the wasteland.
You had the camel follow the instructions, but you've barely left your starting
position. It's going to take significantly more steps to escape!

What if the map isn't for people - what if the map is for ghosts? Are ghosts
even bound by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious
fact: the number of nodes with names ending in `A` is equal to the number ending
in `Z`! If you were a ghost, you'd probably just start at every node that ends
with A and follow all of the paths at the same time until they all
simultaneously end up at nodes that end with `Z`.

For example:

```
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
```

Here, there are two starting nodes, `11A` and `22A` (because they both end with
`A`). As you follow each left/right instruction, use that instruction to
simultaneously navigate away from both nodes you're currently on. Repeat this
process until all of the nodes you're currently on end with `Z`. (If only some
of the nodes you're on end with `Z`, they act like any other node and you
continue as normal.) In this example, you would proceed as follows:

- Step 0: You are at `11A` and `22A`.
- Step 1: You choose all of the left paths, leading you to `11B` and `22B`.
- Step 2: You choose all of the right paths, leading you to `11Z` and `22C`.
- Step 3: You choose all of the left paths, leading you to `11B` and `22Z`.
- Step 4: You choose all of the right paths, leading you to `11Z` and `22B`.
- Step 5: You choose all of the left paths, leading you to `11B` and `22C`.
- Step 6: You choose all of the right paths, leading you to `11Z` and `22Z`.

So, in this example, you end up entirely on nodes that end in `Z` after `6`
steps.

Simultaneously start on every node that ends with `A`. How many steps does it
take before you're only on nodes that end with Z?
"""

import itertools
import math
import re
from functools import partial
from multiprocessing import Pool, cpu_count
from typing import Iterator, Mapping

from aocd import get_data

DATA = get_data(year=2023, day=8)


def parse_input(data: str) -> tuple[str, dict[str, tuple[str, str]]]:
    """Parse the input.

    :param data: The input.
    """
    method, _, *nodes = data.splitlines()

    node_map = {}
    for node in nodes:
        if match := re.match(r"(\w+) = \((\w+), (\w+)\)", node):
            node_map[match.group(1)] = (match.group(2), match.group(3))
        else:
            raise ValueError(f"Error parsing map: {node}")

    return method, node_map


def traverse(
    start: str, end: str | None, method: str, node_map: Mapping[str, tuple[str, str]]
) -> Iterator[str]:
    """ """
    t_map = {"L": 0, "R": 1}

    current = start
    method_index = 0
    while end is None or current != end:
        current = node_map[current][t_map[method[method_index]]]
        yield current
        method_index = (method_index + 1) % len(method)


def get_loop(
    start: str, method: str, node_map: Mapping[str, tuple[str, str]]
) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    """Get the loop for a particular starting point.

    :param start: The starting node.
    :param method: The instructions for the map.
    :param node_map: The node mapping.
    :returns: The initial and loop sequence for the node.
    """
    t_map = {"L": 0, "R": 1}

    path = []

    current = start
    method_index = 0
    while True:
        instruction = (current, method_index)
        if instruction in path:
            break
        path.append(instruction)

        current = node_map[current][t_map[method[method_index]]]
        method_index = (method_index + 1) % len(method)

    return path[:method_index], path[method_index:]


def part1(data: str = DATA) -> int:
    """Solve Part 1.

    :param data: The input data.
    :returns: The solution.
    """
    method, node_map = parse_input(data)
    return len(list(traverse("AAA", "ZZZ", method, node_map)))


def part2(data: str = DATA) -> int:
    """Solve Part 2.

    :param data: The input data.
    :returns: The solution.
    """
    method, node_map = parse_input(data)

    # For each starting point, break it down to the initial sequence and the
    # sequence that loops.
    with Pool(processes=cpu_count()) as pool:
        loops = pool.map(
            partial(get_loop, method=method, node_map=node_map),
            [n for n in node_map if n.endswith("A")],
        )

    # For each starting point, find the points in the loop at which an entry
    # ending with Z is found.
    z_offsets = [
        [len(initial) + loop.index(n) for n in loop if n[0].endswith("Z")]
        for initial, loop in loops
    ]

    # Return the smallest LCM combination of z-offsets
    return min(math.lcm(*c) for c in itertools.product(*z_offsets))
