Advent of Code
==============

This repository contains solution code for the [Advent of Code][aoc].

Organization
------------

Solutions for a given day and year should be organized into the following
heirarchy:

```
.
└── aoc
    └── aoc_{YYYY}
        ├── __init__.py
        ├── advent_{YYYY}_{DD}.py
        ├── test_{YYYY}_{DD}.py
        └── ...
```

Each day will have its own module, and the solution code for each part of the
day should be in functions named `part1` and `part2`, which can accept no
arguments. The test modules should have test functions named `test_part_1` and
`test_part_2`.

This repository uses the `advent-of-code-data` library, which requires the
`AOC_SESSION` environment variable to be set with the session key from the
browser in order to download the data. This should be set the the file `.env`,
which should not be checked in.

[aoc]: https://adventofcode.com

