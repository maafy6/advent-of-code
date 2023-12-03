"""Advent of Code 2015 - Day 11

Day 11: Corporate Policy
========================

Santa's previous password expired, and he needs help choosing a new one.

To help him remember his new password after the old one expires, Santa has
devised a method of coming up with a password based on the previous one.
Corporate policy dictates that passwords must be exactly eight lowercase
letters (for security reasons), so he finds his new password by incrementing
his old password string repeatedly until it is valid.

Incrementing is just like counting with numbers: `xx`, `xy`, `xz`, `ya`, `yb`,
and so on. Increase the rightmost letter one step; if it was `z`, it wraps
around to `a`, and repeat with the next letter to the left until one doesn't
wrap around.

Unfortunately for Santa, a new Security-Elf recently started, and he has
imposed some additional password requirements:

- Passwords must include one increasing straight of at least three letters,
    like `abc`, `bcd`, `cde`, and so on, up to `xyz`. They cannot skip letters;
    `abd` doesn't count.
- Passwords may not contain the letters `i`, `o`, or `l`, as these letters can
    be mistaken for other characters and are therefore confusing.
- Passwords must contain at least two different, non-overlapping pairs of
    letters, like `aa`, `bb`, or `zz`.

For example:

- `hijklmmn` meets the first requirement (because it contains the straight
    `hij`) but fails the second requirement requirement (because it contains
    `i` and `l`).
- `abbceffg` meets the third requirement (because it repeats `bb` and `ff`) but
    fails the first requirement.
- `abbcegjk` fails the third requirement, because it only has one double letter
    (`bb`).
- The next password after `abcdefgh` is `abcdffaa`.
- The next password after `ghijklmn` is `ghjaabcc`, because you eventually skip
    all the passwords that start with `ghi...`, since `i` is not allowed.

Given Santa's current password (your puzzle input), what should his next
password be?

Part Two
========

Santa's password expired again. What's the next one?
"""

import re

from aocd import get_data
from typing_extensions import Self

DATA = get_data(year=2015, day=11)


class Password(str):
    """Class for manipulating passwords."""

    def increment(self) -> Self:
        """Increment the password."""
        last_char = chr(((ord(self[-1]) - 97 + 1) % 26) + 97)
        return Password(
            (Password(self[:-1]).increment() if last_char == "a" else self[:-1])
            + last_char
        )

    def is_valid(self) -> bool:
        """Return true if valid."""
        if len(self) != 8:
            return False
        if self != self.lower():
            return False

        if any(forbidden in self for forbidden in "ilo"):
            return False

        for i in range(len(self) - 2):
            if (
                ord(self[i]) == ord(self[i + 1]) - 1
                and ord(self[i + 1]) == ord(self[i + 2]) - 1
            ):
                break
        else:
            return False

        doubles = set()
        for i in range(len(self) - 1):
            if self[i] == self[i + 1]:
                doubles.add(self[i])

        if len(doubles) < 2:
            return False

        return True

    def next_valid(self) -> Self:
        """Return the next valid password."""
        # If the password contains a forbidden letter, skip to where the first
        # forbidden letter in the string would be incremented.
        if match := re.search(r"[ilo]", self):
            next_base = Password(self[: match.start() + 1]).increment()
            next_password = Password(next_base + "a" * (len(self) - match.start() - 1))
        else:
            next_password = self.increment()

        while not next_password.is_valid():
            next_password = next_password.increment()

        return next_password


def part1(data: str = DATA) -> str:
    """Solve part 1.

    :param data: The input data.
    :returns: The next password.
    """
    p = Password(data)
    return p.next_valid()


def part2(data: str = DATA) -> str:
    """Solve part 2.

    :param data: The input data.
    :returns: The next next password.
    """
    p = Password(part1(data))
    return p.next_valid()
