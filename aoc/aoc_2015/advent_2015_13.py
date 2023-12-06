"""Advent of Code 2015 - Day 13

Day 13: Knights of the Dinner Table
===================================

In years past, the holiday feast with your family hasn't gone so well. Not
everyone gets along! This year, you resolve, will be different. You're going to
find the optimal seating arrangement and avoid all those awkward conversations.

You start by writing up a list of everyone invited and the amount their
happiness would increase or decrease if they were to find themselves sitting
next to each other person. You have a circular table that will be just big
enough to fit everyone comfortably, and so each person will have exactly two
neighbors.

For example, suppose you have only four attendees planned, and you calculate
their potential happiness as follows:

```
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
```

Then, if you seat Alice next to David, Alice would lose `2` happiness units
(because David talks so much), but David would gain `46` happiness units
(because Alice is such a good listener), for a total change of `44`.

If you continue around the table, you could then seat Bob next to Alice (Bob
gains `83`, Alice gains `54`). Finally, seat Carol, who sits next to Bob (Carol
gains `60`, Bob loses `7`) and David (Carol gains `55`, David gains `41`). The
arrangement looks like this:

```
     +41 +46
+55   David    -2
Carol       Alice
+60    Bob    +54
     -7  +83
```

After trying every other seating arrangement in this hypothetical scenario, you
find that this one is the most optimal, with a total change in happiness of
``330``.

What is the total change in happiness for the optimal seating arrangement of
the actual guest list?

Part Two
========

In all the commotion, you realize that you forgot to seat yourself. At this
point, you're pretty apathetic toward the whole thing, and your happiness
wouldn't really go up or down regardless of who you sit next to. You assume
everyone else would be just as ambivalent about sitting next to you, too.

So, add yourself to the list, and give all happiness relationships that involve
you a score of `0`.

What is the total change in happiness for the optimal seating arrangement that
actually includes yourself?
"""

import re
from collections import defaultdict
from copy import copy
from typing import Mapping, Optional, MutableSequence, Iterator, Tuple

from aocd import get_data

DATA = get_data(year=2015, day=13)


def get_happiness_map(data: str) -> Mapping[str, Mapping[str, int]]:
    """Build a mapping indicating happiness effects between neighbors.

    :param data: The happiness data.
    :returns: The happiness effect mapping.
    """
    happiness = defaultdict(lambda: defaultdict(int))
    for line in data.splitlines():
        if match := re.match(
            r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).",
            line.strip(),
        ):
            happiness[match.group(1)][match.group(4)] = int(match.group(3)) * (
                1 if match.group(2) == "gain" else -1
            )

    return happiness


def gen_table(
    attendees: MutableSequence[str],
    happiness_map: Mapping[str, Mapping[str, int]],
    *,
    table: Optional[MutableSequence[str]] = None,
    happiness_score: int = 0,
) -> Iterator[Tuple[MutableSequence[str], int]]:
    """Generate routes traversing all nodes.

    :param attendees: A list of unseated attendees.
    :param distances: A mapping of happiness effects.
    :table: The current table as traversed so far.
    :happiness_score: The distance traversed by the current route.
    """
    if not attendees:
        if table:
            happiness_score += (
                happiness_map[table[-1]][table[0]] + happiness_map[table[0]][table[-1]]
            )
        yield table, happiness_score

    if not table:
        table = []

    for node in attendees:
        if table:
            sub_route_score = (
                happiness_score
                + happiness_map[table[-1]][node]
                + happiness_map[node][table[-1]]
            )
        else:
            sub_route_score = 0

        sub_nodes = copy(attendees)
        sub_nodes.remove(node)
        sub_route = copy(table)
        sub_route.append(node)

        yield from gen_table(
            sub_nodes,
            happiness_map,
            table=sub_route,
            happiness_score=sub_route_score,
        )


def part1(data: str = DATA) -> int:
    """Solve part 1.

    :param data: The input data.
    :returns: The total happiness.
    """
    happiness_map = get_happiness_map(data)
    attendees = sorted(list(happiness_map.keys()))

    max_happiness = 0
    for _, happiness in gen_table(attendees, happiness_map):
        max_happiness = max(max_happiness, happiness)

    return max_happiness


def part2(data: str = DATA) -> int:
    """Solve part 2.

    :param data: The input data.
    :returns: The total happiness.
    """
    happiness_map = get_happiness_map(data)
    attendees = sorted(list(happiness_map.keys()))
    for a in attendees:
        happiness_map[""][a] = 0
        happiness_map[a][""] = 0
    attendees.append("")

    max_happiness = 0
    for _, happiness in gen_table(attendees, happiness_map):
        max_happiness = max(max_happiness, happiness)

    return max_happiness
