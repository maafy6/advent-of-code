"""Advent of Code 2015: Day 19

Day 19: Medicine for Rudolph
============================

Rudolph the Red-Nosed Reindeer is sick! His nose isn't shining very brightly,
and he needs medicine.

Red-Nosed Reindeer biology isn't similar to regular reindeer biology; Rudolph
is going to need custom-made medicine. Unfortunately, Red-Nosed Reindeer
chemistry isn't similar to regular reindeer chemistry, either.

The North Pole is equipped with a Red-Nosed Reindeer nuclear fusion/fission
plant, capable of constructing any Red-Nosed Reindeer molecule you need. It
works by starting with some input molecule and then doing a series of
replacements, one per step, until it has the right molecule.

However, the machine has to be calibrated before it can be used. Calibration
involves determining the number of molecules that can be generated in one step
from a given starting point.

For example, imagine a simpler machine that supports only the following
replacements:

```
H => HO
H => OH
O => HH
```

Given the replacements above and starting with `HOH`, the following molecules
could be generated:

- `HOOH` (via `H => HO` on the first `H`).
- `HOHO` (via `H => HO` on the second `H`).
- `OHOH` (via `H => OH` on the first `H`).
- `HOOH` (via `H => OH` on the second `H`).
- `HHHH` (via `O => HH`).

So, in the example above, there are `4` distinct molecules (not five, because
`HOOH` appears twice) after one replacement from `HOH`. Santa's favorite
molecule, `HOHOHO`, can become `7` distinct molecules (over nine replacements:
six from `H`, and three from `O`).

The machine replaces without regard for the surrounding characters. For
example, given the string `H2O`, the transition H => OO would result in `OO2O`.

Your puzzle input describes all of the possible replacements and, at the
bottom, the medicine molecule for which you need to calibrate the machine. How
many distinct molecules can be created after all the different ways you can do
one replacement on the medicine molecule?

Part Two
========

Now that the machine is calibrated, you're ready to begin molecule fabrication.

Molecule fabrication always begins with just a single electron, `e`, and
applying replacements one at a time, just like the ones during calibration.

For example, suppose you have the following replacements:

`````
e => H
e => O
H => HO
H => OH
O => HH
```

If you'd like to make `HOH`, you start with `e`, and then make the following
replacements:

- `e => O` to get `O`
- `O => HH` to get `HH`
- `H => OH` (on the second `H`) to get `HOH`

So, you could make `HOH` after `3` steps. Santa's favorite molecule, `HOHOHO`,
can be made in `6` steps.

How long will it take to make the medicine? Given the available replacements
and the medicine molecule in your puzzle input, what is the fewest number of
steps to go from e to the medicine molecule?
"""

import re
from collections import defaultdict
from typing import Iterator, Mapping, Sequence, Tuple

from aocd import get_data

DATA = get_data(year=2015, day=19)


def parse_input(data: str) -> Tuple[Mapping[str, Sequence[str]], str]:
    """Parse the input string.

    :param data: The inputer data.
    :returns: A tuple containing the replacements mapping and the molecule.
    """
    replacement_data, molecule = data.split("\n\n")

    replacements = defaultdict(list)
    for rep_data in replacement_data.splitlines():
        source, dest = rep_data.split(" => ")
        replacements[source].append(dest)

    return replacements, molecule


def gen_replacements(
    molecule: str, replacements: Mapping[str, Sequence[str]]
) -> Iterator[str]:
    """Get all single replacements for a molecule.

    :param molecule: The initial molecule.
    :param replacements: The replacement mapping.
    :yields: Molecules which may be derived from this in one step.
    """
    for source in replacements:
        for match in re.finditer(source, molecule):
            for dest in replacements[source]:
                yield molecule[: match.start()] + dest + molecule[match.end() :]


def devolve_molecule(
    molecule: str, replacements: Mapping[str, Sequence[str]]
) -> Iterator[str]:
    """Get all devolutions of a molecule.

    :param molecule: The initial molecule.
    :param replacements: The replacement mapping.
    :yields: Molecules which may have generated this molecule.
    """
    for source in replacements:
        for dest in replacements[source]:
            for match in re.finditer(dest, molecule):
                yield molecule[: match.start()] + source + molecule[match.end() :]


def devolve_mapping(
    replacements: Mapping[str, Sequence[str]]
) -> Mapping[str, Sequence[str]]:
    """Return a devolution mapping products to their source.

    :param replacements: The forward mapping.
    :returns: The reverse mapping.
    """
    devolve = {}
    for source in replacements:
        for dest in replacements[source]:
            if dest in devolve:
                raise KeyError
            devolve[dest] = source

    return devolve


def part1(data: str = DATA) -> int:
    """Solve part 1.

    :param data: The input data.
    :returns: The number of distinct molecules after 1 replacement.
    """
    replacements, molecule = parse_input(data)
    new_molecules = set(rep for rep in gen_replacements(molecule, replacements))
    return len(new_molecules)


def part2(data: str = DATA) -> int:
    """Solve part 2.

    :param data: The input data.
    :returns: The fewest steps to reach the target molecule.
    """
    replacements, source = parse_input(data)

    # Try the greedy approach first - always apply the devolution that shrinks
    # the molecule the most. (Even this implementation is a little bit lazy,
    # it only tries to apply the devolution with the largest output, but
    # doesn't count the number of tokens the string is reduced by.)
    devolve = devolve_mapping(replacements)
    i = 0
    while source != "e":
        for dsrc in sorted(devolve, key=len, reverse=True):
            if dsrc in source:
                source = re.sub(dsrc, devolve[dsrc], source, 1)
                i += 1
                break
        else:
            raise ValueError("No devolution available.")

    return i
