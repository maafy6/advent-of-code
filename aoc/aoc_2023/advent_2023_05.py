"""Advent of Code 2023: Day 5

Day 5: If You Give A Seed A Fertilizer
======================================

You take the boat and find the gardener right where you were told he would be:
managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow
Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with!
Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand
soon; we only turned off the water a few days... weeks... oh no." His face sinks
into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot
to check why we stopped getting more sand! There's a ferry leaving soon that is
headed over in that direction - it's much faster than your boat. Could you
please go check it out?"

You barely have time to agree to this request when he brings up another. "While
you wait for the ferry, maybe you can help us with our food production problem.
The latest Island Island Almanac just arrived and we're having trouble making
sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted.
It also lists what type of soil to use with each kind of seed, what type of
fertilizer to use with each kind of soil, what type of water to use with each
kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is
identified with a number, but numbers are reused by each category - that is,
soil `123` and fertilizer `123` aren't necessarily related to each other.

For example:

```
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
```

The almanac starts by listing which seeds need to be planted: seeds `79`, `14`,
`55`, and `13`.

The rest of the almanac contains a list of maps which describe how to convert
numbers from a source category into numbers in a destination category. That is,
the section that starts with `seed-to-soil map:` describes how to convert a seed
number (the source) to a soil number (the destination). This lets the gardener
and his team know which soil to use with which seeds, which water to use with
which fertilizer, and so on.

Rather than list every source number and its corresponding destination number
one by one, the maps describe entire ranges of numbers that can be converted.
Each line within a map contains three numbers: the destination range start, the
source range start, and the range length.

Consider again the example `seed-to-soil map`:

```
50 98 2
52 50 48
```

The first line has a destination range start of `50`, a source range start of
`98`, and a range length of `2`. This line means that the source range starts at
`98` and contains two values: `98` and `99`. The destination range is the same
length, but it starts at `50`, so its two values are `50` and `51`. With this
information, you know that seed number `98` corresponds to soil number `50` and
that seed number `99` corresponds to soil number `51`.

The second line means that the source range starts at `50` and contains `48`
values: `50`, `51`, ..., `96`, `97`. This corresponds to a destination range
starting at `52` and also containing `48` values: `52`, `53`, ..., `98`, `99`.
So, seed number `53` corresponds to soil number `55`.

Any source numbers that aren't mapped correspond to the same destination number.
So, seed number `10` corresponds to soil number `10`.

So, the entire list of seed numbers and their corresponding soil numbers looks
like this:

```
seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
```

With this map, you can look up the soil number required for each initial seed
number:

- Seed number `79` corresponds to soil number `81`.
- Seed number `14` corresponds to soil number `14`.
- Seed number `55` corresponds to soil number `57`.
- Seed number `13` corresponds to soil number `13`.

The gardener and his team want to get started as soon as possible, so they'd
like to know the closest location that needs a seed. Using these maps, find the
lowest location number that corresponds to any of the initial seeds. To do this,
you'll need to convert each seed number through other categories until you can
find its corresponding location number. In this example, the corresponding types
are:

- Seed `79`, soil `81`, fertilizer `81`, water `81`, light `74`, temperature
    `78`, humidity `78`, location 82.
- Seed `14`, soil `14`, fertilizer `53`, water `49`, light `42`, temperature
    `42`, humidity `43`, location 43.
- Seed `55`, soil `57`, fertilizer `57`, water `53`, light `46`, temperature
    `82`, humidity `82`, location 86.
- Seed `13`, soil `13`, fertilizer `52`, water `41`, light `34`, temperature
    `34`, humidity `35`, location 35.

So, the lowest location number in this example is `35`.

What is the lowest location number that corresponds to any of the initial seed
numbers?

Part Two
========

Everyone will starve if you only plant such a small number of seeds. Re-reading
the almanac, it looks like the `seeds:` line actually describes ranges of seed
numbers.

The values on the initial `seeds:` line come in pairs. Within each pair, the
first value is the start of the range and the second value is the length of the
range. So, in the first line of the example above:

```
seeds: 79 14 55 13```

This line describes two ranges of seed numbers to be planted in the garden. The
first range starts with seed number `79` and contains `14` values: `79`, `80`,
..., `91`, `92`. The second range starts with seed number `55` and contains `13`
values: `55`, `56`, ..., `66`, `67`.

Now, rather than considering four seed numbers, you need to consider a total of
27 seed numbers.

In the above example, the lowest location number can be obtained from seed
number `82`, which corresponds to soil `84`, fertilizer `84`, water `84`, light
`77`, temperature `45`, humidity `46`, and location 46. So, the lowest location
number is `46`.

Consider all of the initial seed numbers listed in the ranges on the first line
of the almanac. What is the lowest location number that corresponds to any of
the initial seed numbers?
"""

import math
from dataclasses import dataclass
from typing import Iterable, Iterator, Mapping, Optional, Sequence, Tuple

from aocd import get_data

DATA = get_data(year=2023, day=5)


@dataclass
class PipeRange:
    """Model the range and effect of a portion of a pipe."""

    start: int
    end: int
    offset: int

    def fed_from(self, other: "PipeRange") -> Optional["PipeRange"]:
        """Return the portion of the other pipeline that feeds this pipeline.

        :param other: The pipeline used to feed this pipe.
        :returns: The portion of other which has outputs corresponding to the
            inputs of this pipe, or `None` if there is no overlap.
        """
        output_start = other.start + other.offset
        output_end = other.end + other.offset

        new_start = max(self.start, output_start)
        new_end = min(self.end, output_end)

        if new_end <= new_start:
            return None

        return PipeRange(
            new_start - other.offset,
            new_end - other.offset,
            other.offset,
        )


class Pipe:
    """Model for a pipe."""

    def __init__(self, name: str, ranges: Iterable[PipeRange], fill_gaps: bool = True):
        """Initialize the pipe.

        :param name: The name of the pipe.
        :param ranges: A set of ranges that affect the output of the pipe.
        :param fill_gaps: If `True`, include no-op portions of the pipe (e.g.
            `offset=0` in the pipe ranges.)
        """
        self.name = name
        self.ranges = (
            self._fill_ranges(ranges)
            if fill_gaps
            else sorted(ranges, key=lambda r: r.start)
        )

    def _fill_ranges(self, ranges: Iterable[PipeRange]) -> Sequence[PipeRange]:
        """Provide pipe ranges with any gaps filled in with 0-offset ranges.

        :param ranges: The initial ranges.
        :returns: A set of pipe ranges covering all positive integers.
        """
        if not ranges:
            return [PipeRange(0, math.inf, 0)]

        pipe_ranges = []
        boundaries = set()
        last_end = 0
        for pipe_range in sorted(ranges, key=lambda r: r.start):
            if pipe_range.start not in boundaries:
                pipe_ranges.append(PipeRange(last_end, pipe_range.start, 0))
            pipe_ranges.append(pipe_range)
            last_end = pipe_range.end

        pipe_ranges.append(PipeRange(last_end, math.inf, 0))
        return pipe_ranges

    def __getitem__(self, key: int) -> int:
        """Get the output value for the pipe.

        :param key: The input value.
        :returns: The pipe output.
        """
        for src_range in self.ranges:
            if src_range.start <= key < src_range.end:
                return key + src_range.offset

        return key

    @classmethod
    def loads(cls, desc: str) -> "Pipe":
        """Load the pipe data from a string.

        :param desc: The pipe description.
        :returns: A new Pipe.
        """
        name = None
        ranges = []
        for line in desc.splitlines():
            if name is None:
                name = line
            else:
                dest, source, count = [int(n) for n in line.split()]
                source_range = PipeRange(source, source + count, dest - source)
                ranges.append(source_range)

        return cls(name, ranges)


def map_pipeline(value: int, pipeline: Sequence[Mapping[int, int]]) -> int:
    """Run the value through the full pipeline.

    :param value: The input value.
    :param pipeline: The sequence of pipes to apply the value to.
    :returns: The output value of the pipeline.
    """
    for pipe in pipeline:
        value = pipe[value]

    return value


def parse_input(data: str) -> Tuple[Sequence[int], Sequence[Mapping[int, int]]]:
    """Parse the input data.

    :param data: The input data.
    :returns: A tuple containing a list of seeds and the pipeline to run them through.
    """
    seeds = []
    pipeline = []
    current_pipe_data = None
    for line in data.splitlines():
        if line.startswith("seeds:"):
            seeds.extend([int(s) for s in line.split(":")[1].split()])

        if line.endswith("map:"):
            current_pipe_data = [line]
        elif current_pipe_data is not None:
            if line:
                current_pipe_data.append(line)
            else:
                pipeline.append(Pipe.loads("\n".join(current_pipe_data)))
                current_pipe_data = []

    if current_pipe_data:
        pipeline.append(Pipe.loads("\n".join(current_pipe_data)))
        current_pipe_data = []

    return seeds, pipeline


def get_seed_ranges(
    pipeline: Sequence[Pipe], output_ranges: Optional[Iterable[PipeRange]] = None
) -> Iterator[PipeRange]:
    """Yield initial input ranges.

    The ranges will be sorted so that the first output range yielded maps to
    the lowest final output.

    :param pipeline: The full pipeline to evaluate.
    :param output_ranges: The currenty examined output ranges.
    :yields: Seed input ranges.
    """
    # Final case - no more pipeline to evaluate
    if not pipeline:
        yield from output_ranges
        return

    pipe = pipeline[-1]
    pipe_ranges = sorted(pipe.ranges, key=lambda r: r.start + r.offset)

    # Initial case, generate the first set of output ranges
    if output_ranges is None:
        yield from get_seed_ranges(pipeline[:-1], pipe_ranges)
        return

    # Middle cases - yield the portion of the ranges in the last pipe in the
    # pipeline that map to an output range.
    for output_range in output_ranges:
        feeder_pipes = [
            output_range.fed_from(pipe_range)
            for pipe_range in pipe_ranges
            if output_range.fed_from(pipe_range) is not None
        ]
        if feeder_pipes:
            yield from get_seed_ranges(pipeline[:-1], feeder_pipes)


def part1(data: str = DATA) -> int:
    """Solve Part 1.

    :param data: The input data.
    :returns: The solution.
    """
    seeds, pipeline = parse_input(data)
    return min(map_pipeline(s, pipeline) for s in seeds)


def part2(data: str = DATA) -> int:
    """Solve Part 2.

    :param data: The input data.
    :returns: The solution.
    """
    seeds, pipeline = parse_input(data)

    seed_ranges = [
        PipeRange(seeds[i], seeds[i] + seeds[i + 1], 0) for i in range(0, len(seeds), 2)
    ]
    seed_pipe = Pipe("seeds", seed_ranges, fill_gaps=False)

    # The ranges should be sorted according to the final output they
    # produce, so we can just return the evaluation of the first yield.
    for seed_range in get_seed_ranges([seed_pipe] + pipeline):
        return map_pipeline(seed_range.start, pipeline)
