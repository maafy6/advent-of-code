"""Advent of Code 2023: Day 13

Day 13: Point of Incidence
==========================

With your help, the hot springs team locates an appropriate spring which
launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray
mountains scattered around. After a while, you make your way to a nearby cluster
of mountains only to discover that the valley between them is completely full of
large mirrors.  Most of the mirrors seem to be aligned in a consistent way;
perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have
fallen from the large metal frames keeping them in place. The mirrors are
extremely flat and shiny, and many of the fallen mirrors have lodged into the
ash at strange angles. Because the terrain is all one color, it's hard to tell
where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (`.`) and rocks (`#`) that you see as you walk
(your puzzle input); perhaps by carefully analyzing these patterns, you can
figure out where the mirrors are!

For example:

```
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
```

To find the reflection in each pattern, you need to find a perfect reflection
across either a horizontal line between two rows or across a vertical line
between two columns.

In the first pattern, the reflection is across a vertical line between two
columns; arrows on each of the two columns point at the line between the
columns:

```
123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789
```

In this pattern, the line of reflection is the vertical line between columns 5
and 6. Because the vertical line is not perfectly in the middle of the pattern,
part of the pattern (column 1) has nowhere to reflect onto and can be ignored;
every other column has a reflected column within the pattern and must match
exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5
matches 6.

The second pattern reflects across a horizontal line instead:

```
1 #...##..# 1  0
2 #....#..# 2  1
3 ..##..### 3  2
4v#####.##.v4  3
5^#####.##.^5  4
6 ..##..### 6  5
7 #....#..# 7  6
```

This pattern reflects across the horizontal line between rows 4 and 5. Row 1
would reflect with a hypothetical row 8, but since that's not in the pattern,
row 1 doesn't need to match anything. The remaining rows match: row 2 matches
row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of
each vertical line of reflection; to that, also add 100 multiplied by the number
of rows above each horizontal line of reflection. In the above example, the
first pattern's vertical line has `5` columns to its left and the second
pattern's horizontal line has `4` rows above it, a total of `405`.

Find the line of reflection in each of the patterns in your notes. What number
do you get after summarizing all of your notes?

Part Two
========

You resume walking through the valley of mirrors and - SMACK! - run directly
into one. Hopefully nobody was watching, because that must have been pretty
embarrassing.

Upon closer inspection, you discover that every mirror has exactly one smudge:
exactly one `.` or `#` should be the opposite type.

In each pattern, you'll need to locate and fix the smudge that causes a
different reflection line to be valid. (The old reflection line won't
necessarily continue being valid after the smudge is fixed.)

Here's the above example again:

```
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
```

The first pattern's smudge is in the top-left corner. If the top-left `#` were
instead `.`, it would have a different, horizontal line of reflection:

```
1 ..##..##. 1
2 ..#.##.#. 2
3v##......#v3
4^##......#^4
5 ..#.##.#. 5
6 ..##..##. 6
7 #.#.##.#. 7
```

With the smudge in the top-left corner repaired, a new horizontal line of
reflection between rows 3 and 4 now exists. Row 7 has no corresponding reflected
row and can be ignored, but every other row matches exactly: row 1 matches row
6, row 2 matches row 5, and row 3 matches row 4.

In the second pattern, the smudge can be fixed by changing the fifth symbol on
row 2 from `.` to `#`:

```
1v#...##..#v1
2^#...##..#^2
3 ..##..### 3
4 #####.##. 4
5 #####.##. 5
6 ..##..### 6
7 #....#..# 7
```

Now, the pattern has a different horizontal line of reflection between rows 1
and 2.

Summarize your notes as before, but instead use the new different reflection
lines. In this example, the first pattern's new horizontal line has 3 rows above
it and the second pattern's new horizontal line has 1 row above it, summarizing
to the value `400`.

In each pattern, fix the smudge and find the different line of reflection. What
number do you get after summarizing the new reflection line in each pattern in
your notes?"""

from collections.abc import Iterable, Iterator
from typing import Any

from aocd import get_data

DATA = get_data(year=2023, day=13)


def parse_input(data: str) -> Iterator[list[str]]:
    """Parse the input.

    :param data: The input data.
    :yields: Lists of strings corresponding to a single mirror.
    """
    mirror = []
    for line in data.splitlines():
        if not line:
            yield mirror
            mirror = []
            continue

        mirror.append(line)

    if mirror:
        yield mirror


def count_diffs(i1: Iterable[Any], i2: Iterable[Any]) -> int:
    """Count the number of different items in the two iterables.

    :param i1: The first iterable.
    :param i2: The second iterable.
    :returns: The number of different items at the same position in the
        sequence in the two iterables.
    """
    return sum(1 if v1 != v2 else 0 for v1, v2 in zip(i1, i2))


def get_reflections(mirror: list[str], smudges: int = 0) -> tuple[int, int]:
    """Get the reflection points in the mirror.

    :param mirror: The mirror.
    :param smudges: The number of smudges on the mirror.
    :returns: A tuple of `(row, col)` indicating the reflection point on the
        mirror. If either value is 0, then there is no reflection point on
        that axis.
    """
    row, col = 0, 0

    # This function makes the assumption that it's possible that a row and col
    # can both be mirrored, but it doesn't seem like that's the case in the
    # input data. It also assumes that there will only be one row or column
    # which is reflected in a given mirror, e.g. none of the mirrors look like
    # the following, in which case every row/column is mirrored.
    #
    #   ....
    #   ....
    #   ....
    #   ....

    # If there is a mirroring on either row or column, then each mirrored pair
    # of rows/cols will have the same sum which will be an odd number randing
    # from 1 (0,1) to (2*(len-1) - 1) (in the example below, either 15 for
    # columns (7,8) or 13 for rows (5,6). All possible pairs with the same sum
    # need to be considered (e.g. (4,5), (3,6), (2,7), (1,8)).
    #
    # The indexes here are for the array index - this is one lower than the
    # index required by the problem, which can be calculated as (sum + 1) // 2.
    #
    #    012345678
    #  0 ..##..##.
    #  1 ..#.##.#.
    #  2 ##......#
    #  3 ##......#
    #  4 ..#.##.#.
    #  5 ..##..##.
    #  6 #.#.##.#.

    for rsum in range(1, 2 * (len(mirror) - 1), 2):
        if (
            sum(
                count_diffs(mirror[lo], mirror[rsum - lo])
                for lo in range(rsum // 2 + 1)
                if rsum - lo < len(mirror)
            )
            == smudges
        ):
            row = (rsum + 1) // 2
            break

    width = len(mirror[0])
    for csum in range(1, 2 * (width - 1), 2):
        if (
            sum(
                count_diffs(mirror_row[lo], mirror_row[csum - lo])
                for mirror_row in mirror
                for lo in range(csum // 2 + 1)
                if csum - lo < width
            )
            == smudges
        ):
            col = (csum + 1) // 2
            break

    return row, col


def score_mirror(row: int, col: int) -> int:
    """Return the score for a mirror.

    :param row: The row reflection number.
    :param col: The column reflection number.
    :retruns: The mirror score.
    """
    return 100 * row + col


def part1(data: str = DATA) -> int:
    """Solve Part 1.

    :param data: The input data.
    :returns: The solution.
    """
    return sum(score_mirror(*get_reflections(mirror)) for mirror in parse_input(data))


def part2(data: str = DATA) -> int:
    """Solve Part 2.

    :param data: The input data.
    :returns: The solution.
    """
    return sum(
        score_mirror(*get_reflections(mirror, 1)) for mirror in parse_input(data)
    )
