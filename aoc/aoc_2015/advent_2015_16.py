"""Advent of Code 2015 - Day 16

Day 16: Aunt Sue
================

Your Aunt Sue has given you a wonderful gift, and you'd like to send her a
thank you card. However, there's a small problem: she signed it "From, Aunt
Sue".

You have 500 Aunts named "Sue".

So, to avoid sending the card to the wrong person, you need to figure out which
Aunt Sue (which you conveniently number 1 to 500, for sanity) gave you the
gift. You open the present and, as luck would have it, good ol' Aunt Sue got
you a My First Crime Scene Analysis Machine! Just what you wanted. Or needed,
as the case may be.

The My First Crime Scene Analysis Machine (MFCSAM for short) can detect a few
specific compounds in a given sample, as well as how many distinct kinds of
those compounds there are. According to the instructions, these are what the
MFCSAM can detect:

- `children`, by human DNA age analysis.
- `cats`. It doesn't differentiate individual breeds.
- `Several` seemingly random breeds of dog: `samoyeds`, `pomeranians`,
    `akitas`, and `vizslas`.
- `goldfish`. No other kinds of fish.
- `trees`, all in one group.
- `cars`, presumably by exhaust or gasoline or something.
- `perfumes`, which is handy, since many of your Aunts Sue wear a few kinds.

In fact, many of your Aunts Sue have many of these. You put the wrapping from
the gift into the MFCSAM. It beeps inquisitively at you a few times and then
prints out a message on ticker tape:

```
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
```

You make a list of the things you can remember about each Aunt Sue. Things
missing from your list aren't zero - you simply don't remember the value.

What is the number of the Sue that got you the gift?

Part Two
========

As you're about to send the thank you note, something in the MFCSAM's
instructions catches your eye. Apparently, it has an outdated retroencabulator,
and so the output from the machine isn't exact values - some of them indicate
ranges.

In particular, the `cats` and `trees` readings indicates that there are greater
than that many (due to the unpredictable nuclear decay of cat dander and tree
pollen), while the `pomeranians` and `goldfish` readings indicate that there
are fewer than that many (due to the modial interaction of magnetoreluctance).

What is the number of the real Aunt Sue?
"""

import re
from dataclasses import dataclass
from typing import Mapping, Optional

from aocd import get_data
from typing_extensions import Self

DATA = get_data(year=2015, day=16)


@dataclass
class Sue:  # pylint: disable=too-many-instance-attributes
    """Model for Aunts Sue."""

    id: int
    children: Optional[int] = None
    cats: Optional[int] = None
    samoyeds: Optional[int] = None
    pomeranians: Optional[int] = None
    akitas: Optional[int] = None
    vizslas: Optional[int] = None
    goldfish: Optional[int] = None
    trees: Optional[int] = None
    cars: Optional[int] = None
    perfumes: Optional[int] = None

    @classmethod
    def from_desc(cls, desc: str) -> Self:
        """Build an Aunt Sue from the description.

        :param desc: The description.
        :returns: An Aunt Sue model.
        """
        props = {"id": int(re.search(r"Sue (\d+)", desc).group(1))}
        for prop in re.finditer(r"(\w+): (\d+)", desc):
            props[prop.group(1)] = int(prop.group(2))

        return Sue(**props)

    def matches(self, description: Mapping[str, int], part: int) -> bool:
        """Return true if the Sue matches the description.

        :param description: The description.
        :param part: The part of the puzzle.
        :returns: `True` if the Sue matches the description.
        """
        for key, val in description.items():
            prop = getattr(self, key)
            if prop is None:
                continue

            if part == 1:
                if prop != val:
                    return False
            elif part == 2:
                if key in ("cats", "trees"):
                    if prop <= val:
                        return False
                elif key in ("pomeranians", "goldfish"):
                    if val <= prop:
                        return False
                else:
                    if prop != val:
                        return False

        return True


def _solve(data: str, part: int) -> int:
    """Solve the part.

    :param data: The input data.
    :param part: The part ID.
    :returns: The ID of Aunt Sue.
    """
    description = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    sues = [Sue.from_desc(desc) for desc in data.split("\n")]
    matches = [sue for sue in sues if sue.matches(description, part)]
    if len(matches) > 1:
        raise RuntimeError("No unique match.")
    if not matches:
        raise RuntimeError("No matches.")

    return matches[0].id


def part1(data: str = DATA) -> int:
    """Solve part 1.

    :param data: The input data.
    :returns: The ID of the Sue.
    """
    return _solve(data, 1)


def part2(data: str = DATA) -> int:
    """Solve part 2.

    :param data: The input data.
    :returns: The ID of the Sue.
    """
    return _solve(data, 2)
