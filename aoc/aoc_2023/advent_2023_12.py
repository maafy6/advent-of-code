"""Advent of Code 2023: Day 12

Day 12: Hot Springs
===================

You finally reach the hot springs! You can see steam rising from secluded areas
attached to the primary, ornate building.

As you turn to enter, the researcher stops you. "Wait - I thought you were
looking for the hot springs, weren't you?" You indicate that this definitely
looks like hot springs to you.

"Oh, sorry, common mistake! This is actually the onsen! The hot springs are next
door."

You look in the direction the researcher is pointing and suddenly notice the
massive metal helixes towering overhead. "This way!"

It only takes you a few more steps to reach the main gate of the massive fenced-
off area containing the springs. You go through the gate and into a small
administrative building.

"Hello! What brings you to the hot springs today? Sorry they're not very hot
right now; we're having a lava shortage at the moment." You ask about the
missing machine parts for Desert Island.

"Oh, all of Gear Island is currently offline! Nothing is being manufactured at
the moment, not until we get more lava to heat our forges. And our springs. The
springs aren't very springy unless they're hot!"

"Say, could you go up and see why the lava stopped flowing? The springs are too
cold for normal operation, but we should be able to find one springy enough to
launch you up there!"

There's just one problem - many of the springs have fallen into disrepair, so
they're not actually sure which springs would even be safe to use! Worse yet,
their condition records of which springs are damaged (your puzzle input) are
also damaged! You'll need to help them repair the damaged records.

In the giant field just outside, the springs are arranged into rows. For each
row, the condition records show every spring and whether it is operational (`.`)
or damaged (`#`). This is the part of the condition records that is itself
damaged; for some springs, it is simply unknown (`?`) whether the spring is
operational or damaged.

However, the engineer that produced the condition records also duplicated some
of this information in a different format! After the list of springs for a given
row, the size of each contiguous group of damaged springs is listed in the order
those groups appear in the row. This list always accounts for every damaged
spring, and each number is the entire size of its contiguous group (that is,
groups are always separated by at least one operational spring: `####` would
always be `4`, never `2,2`).

So, condition records with no unknown spring conditions might look like this:

```
#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1
```

However, the condition records are partially damaged; some of the springs'
conditions are actually unknown (`?`). For example:

```
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
```

Equipped with this information, it is your job to figure out how many different
arrangements of operational and broken springs fit the given criteria in each
row.

In the first line (`???.### 1,1,3`), there is exactly one way separate groups of
one, one, and three broken springs (in that order) can appear in that row: the
first three unknown springs must be broken, then operational, then broken
(`#.#`), making the whole row `#.#.###`.

The second line is more interesting: `.??..??...?##. 1,1,3` could be a total of
four different arrangements. The last `?` must always be broken (to satisfy the
final contiguous group of three broken springs), and each `??` must hide exactly
one of the two broken springs. (Neither `??` could be both broken springs or
they would form a single contiguous group of two; if that were true, the numbers
afterward would have been `2,3` instead.) Since each `??` can either be `#.` or
`.#`, there are four possible arrangements of springs.

The last line is actually consistent with ten different arrangements! Because
the first number is `3`, the first and second `?` must both be `.` (if either
were `#`, the first number would have to be `4` or higher). However, the
remaining run of unknown spring conditions have many different ways they could
hold groups of two and one broken springs:

```
?###???????? 3,2,1
.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#
```

In this example, the number of possible arrangements for each row is:

- `???.### 1,1,3` - `1` arrangement
- `.??..??...?##. 1,1,3` - `4` arrangements
- `?#?#?#?#?#?#?#? 1,3,1,6` - `1` arrangement
- `????.#...#... 4,1,1` - `1` arrangement
- `????.######..#####. 1,6,5` - `4` arrangements
- `?###???????? 3,2,1` - `10` arrangements

Adding all of the possible arrangement counts together produces a total of `21`
arrangements.

For each row, count all of the different arrangements of operational and broken
springs that meet the given criteria. What is the sum of those counts?

Part Two
========

As you look out at the field of springs, you feel like there are way more
springs than the condition records list. When you examine the records, you
discover that they were actually folded up this whole time!

To unfold the records, on each row, replace the list of spring conditions with
five copies of itself (separated by `?`) and replace the list of contiguous
groups of damaged springs with five copies of itself (separated by `,`).

So, this row:

```
.# 1
```

Would become:

```
.#?.#?.#?.#?.# 1,1,1,1,1
```

The first line of the above example would become:

```
???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3
```

In the above example, after unfolding, the number of possible arrangements for
some rows is now much larger:

- `???.### 1,1,3` - `1` arrangement
- `.??..??...?##. 1,1,3` - `16384` arrangements
- `?#?#?#?#?#?#?#? 1,3,1,6` - `1` arrangement
- `????.#...#... 4,1,1` - `16` arrangements
- `????.######..#####. 1,6,5` - `2500` arrangements
- `?###???????? 3,2,1` - `506250` arrangements

After unfolding, adding all of the possible arrangement counts together produces
`525152`.

Unfold your condition records; what is the new sum of possible arrangement
counts?
"""

from collections.abc import Iterator
from functools import lru_cache
from itertools import groupby

from aocd import get_data
from tqdm import tqdm

DATA = get_data(year=2023, day=12)


def parse_input(data: str) -> Iterator[tuple[str, tuple[int, ...]]]:
    """Parse the text input."""
    for line in data.splitlines():
        record, desc = line.split()
        desc = tuple(int(d) for d in desc.split(","))
        yield record, desc


def describe_nonogram(nono: str) -> tuple[int, ...]:
    """Describe a nonogram according to its sequence of # characters.

    :param nono: The nonogram string.
    :returns: A list of consecutive sequences of #.
    """
    return tuple(sum(1 for _ in g) for c, g in groupby(nono) if c == "#")


def gen_nonograms(
    record: str, desc: tuple[int, ...], prefix: str = ""
) -> Iterator[str]:
    """Generate nonograms matching the record and its description.

    :param record: The record, with wildcard values as ?.
    :param desc: The description of sequences of # characters.
    :param prefix: The solves prefix for this nonogram.
    """
    # If there are no more `#` runs remaining, the rest must all be `.` (or `?`
    # that can be made into `.`).
    if not desc:
        if "#" in record:
            return

        yield prefix + record.replace("?", ".")
        return

    # If there are fewer possible `#` characters than the description requires,
    # abort.
    maybe_hashes = record.count("#") + record.count("?")
    if maybe_hashes < sum(desc):
        return

    # If there are no more free `?` characters, we should just validate the
    # remaining nonogram for validity.
    if "?" not in record or maybe_hashes == sum(desc):
        record = record.replace("?", "#")
        if describe_nonogram(record) == desc:
            yield prefix + record
        return

    # If the record starts with `.`, we can consume it into the prefix and
    # continue parsing.
    while record[0] == ".":
        record = record[1:]
        prefix += "."

    # If the record starts with `#`, then we should verify that the string can
    # consume the entire next run of `#` from the description (plus a buffer
    # `.` character if we are not at the end of the string.)
    if record[0] == "#":
        run = desc[0]

        # There cannot be a `.` in the run of `#`.
        if "." in record[:run]:
            return

        # Consume the next (run+1) characters, which should be all `#` then one
        # `.` If we are at the end of the string, the trailing `.` may not be
        # needed.
        consumed = "#" * run
        if next_char := record[run : run + 1]:
            if next_char == "#":
                return

            consumed += "."

        yield from gen_nonograms(record[len(consumed) :], desc[1:], prefix + consumed)

    # If the record starts with a `?`, try it out as both a `.` and a `#`.
    elif record[0] == "?":
        yield from gen_nonograms(record[1:], desc, prefix + ".")
        yield from gen_nonograms("#" + record[1:], desc, prefix)

    # There shouldn't be any other characters in the record.
    else:
        raise ValueError("Invalid nonogram character.")


@lru_cache
def count_nonograms(record: str, desc: tuple[int, ...]) -> int:
    """Count the number of nonograms that can be produced by the record.

    :param record: The record.
    :param desc: The description of the nonogram.
    :returns: The number of nonograms that can be produced.
    """
    nono_len = len(record)

    # If there are no more description parts, ensure that there are no more
    # remaining `#` characters.
    if not desc:
        return 1 if record.replace("?", ".") == "." * nono_len else 0

    total = 0
    # The minimum length of the nonogram.
    min_length = sum(desc) + len(desc) - 1
    # The length required by the next section of the nonogram.
    next_length = desc[0] + (1 if len(desc) > 1 else 0)

    # Iterate over each possible starting position for the next run of `#` in
    # the nonogram and count the number of nonograms that may be produced from
    # there.
    for i in range(nono_len - min_length + 1):
        # Build the next section of the nonogram from the record, replacing `?`
        # with `#` in the spots that correspond to the run and `.` elsewhere.
        next_section = record[:i].replace("?", ".") + record[i : i + desc[0]].replace(
            "?", "#"
        )
        if len(desc) > 1:
            next_section += record[i + desc[0]].replace("?", ".")

        # Verify that the next section of the nonogram actually matches the
        # expected form.
        if (
            (next_section[:i] != "." * i)
            or (next_section[i : i + desc[0]] != "#" * desc[0])
            or (len(desc) > 1 and next_section[-1] == "#")
        ):
            continue

        total += count_nonograms(record[i + next_length :], desc[1:])

    return total


def count_expanded_nonogram(
    record: str, desc: tuple[int, ...], expansion: int = 1
) -> int:
    """Count the nonograms that can be obtained from the expanded nonogram.

    The nonogram will be expanded by joining the requested number of copies of
    the record with a `?` in between and by joining the requested number of
    copies of the description together.

    :param record: The original record.
    :param desc: The original description.
    :param expansion: The expansion factor.
    :returns: The number of nonograms that can be obtained from the expanded
        nonogram.
    """
    return count_nonograms("?".join([record] * expansion), desc * expansion)


def part1(data: str = DATA) -> int:
    """Solve Part 1.

    :param data: The input data.
    :returns: The solution.
    """
    return sum(
        sum(1 for _ in gen_nonograms(record, desc))
        for record, desc in parse_input(data)
    )


def part2(data: str = DATA) -> int:
    """Solve Part 2.

    :param data: The input data.
    :returns: The solution.
    """
    return sum(
        count_expanded_nonogram(record, desc, 5)
        for record, desc in tqdm(list(parse_input(data)))
    )
