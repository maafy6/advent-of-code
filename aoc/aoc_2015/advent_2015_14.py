"""Advent of Code 2015 - Day 14

Day 14: Reindeer Olympics
=========================

This year is the Reindeer Olympics! Reindeer can fly at high speeds, but must
rest occasionally to recover their energy. Santa would like to know which of
his reindeer is fastest, and so he has them race.

Reindeer can only either be flying (always at their top speed) or resting (not
moving at all), and always spend whole seconds in either state.

For example, suppose you have the following Reindeer:

- Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
- Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

After one second, Comet has gone 14 km, while Dancer has gone 16 km. After ten
seconds, Comet has gone 140 km, while Dancer has gone 160 km. On the eleventh
second, Comet begins resting (staying at 140 km), and Dancer continues on for a
total distance of 176 km. On the 12th second, both reindeer are resting. They
continue to rest until the 138th second, when Comet flies for another ten
seconds. On the 174th second, Dancer flies for another 11 seconds.

In this example, after the 1000th second, both reindeer are resting, and Comet
is in the lead at `1120` km (poor Dancer has only gotten `1056` km by that
point). So, in this situation, Comet would win (if the race ended at 1000
seconds).

Given the descriptions of each reindeer (in your puzzle input), after exactly
`2503` seconds, what distance has the winning reindeer traveled?

Part Two
========

Seeing how reindeer move in bursts, Santa decides he's not pleased with the old
scoring system.

Instead, at the end of each second, he awards one point to the reindeer
currently in the lead. (If there are multiple reindeer tied for the lead, they
each get one point.) He keeps the traditional 2503 second time limit, of
course, as doing otherwise would be entirely ridiculous.

Given the example reindeer from above, after the first second, Dancer is in the
lead and gets one point. He stays in the lead until several seconds into
Comet's second burst: after the 140th second, Comet pulls into the lead and
gets his first point. Of course, since Dancer had been in the lead for the 139
seconds before that, he has accumulated 139 points by the 140th second.

After the 1000th second, Dancer has accumulated `689` points, while poor Comet,
our old champion, only has `312`. So, with the new scoring system, Dancer would
win (if the race ended at 1000 seconds).

Again given the descriptions of each reindeer (in your puzzle input), after
exactly `2503` seconds, how many points does the winning reindeer have?
"""

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Mapping, Sequence

from aocd import get_data
from typing_extensions import Self

DATA = get_data(year=2015, day=14)


@dataclass
class Reindeer:
    """Reindeer model."""

    name: str
    speed: int
    duration: int
    rest: int

    @property
    def cycle_time(self) -> int:
        """Return the total cycle time for the reindeer."""
        return self.duration + self.rest

    @classmethod
    def from_str(cls, desc: str) -> Self:
        """Build a reindeer from a description string.

        :param desc: The description string.
        :returns: A Reindeer.
        :raises ValueError: If the description string does not parse.
        """
        if match := re.match(
            r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.",
            desc,
        ):
            return cls(
                name=match.group(1),
                speed=int(match.group(2)),
                duration=int(match.group(3)),
                rest=int(match.group(4)),
            )

        raise ValueError("Unable to parse reindeer.")


def reindeer_distance(reindeer: Reindeer, time: int) -> int:
    """Calculate the distance traveled by a reindeer.

    :param reindeer: The reindeer.
    :param time: The total time elapsed.
    :returns: The amount of distance covered.
    """
    dist = 0

    full_cycles = time // reindeer.cycle_time
    dist += full_cycles * reindeer.duration * reindeer.speed

    remaining_time = time % reindeer.cycle_time
    last_segment = min(reindeer.duration, remaining_time)
    dist += last_segment * reindeer.speed

    return dist


def part1(data: str = DATA, duration: int = 2503) -> int:
    """Solve part 1.

    :param data: The input data.
    :returns: The distance covered by the reindeer covering the furthest distance.
    """
    return max(
        reindeer_distance(Reindeer.from_str(reindeer), duration)
        for reindeer in data.splitlines()
    )


def reindeer_race(reindeers: Sequence[Reindeer], duration: int) -> Mapping[str, int]:
    """Calculate the scores of a reindeer race.

    :param reindeers: A sequence of Reindeer.
    :param duration: The duration of the race.
    """
    reindeer_positions = defaultdict(int)
    reindeer_scores = defaultdict(int)
    leader_pos = 0
    for t in range(duration):
        for reindeer in reindeers:
            if (t % reindeer.cycle_time) < reindeer.duration:
                reindeer_positions[reindeer.name] += reindeer.speed
                leader_pos = max(leader_pos, reindeer_positions[reindeer.name])

        for reindeer in reindeers:
            if reindeer_positions[reindeer.name] == leader_pos:
                reindeer_scores[reindeer.name] += 1

    return reindeer_scores


def part2(data: str = DATA, duration: int = 2503) -> int:
    """Solve part 2.

    :param data: The input data.
    :returns: The winner score.
    """
    reindeers = [Reindeer.from_str(desc) for desc in data.splitlines()]
    scores = reindeer_race(reindeers, duration)
    return max(scores.values())
