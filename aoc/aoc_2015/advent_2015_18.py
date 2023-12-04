"""Advent of Code 2015 - Day 18

Day 18: Like a GIF For Your Yard
================================

After the million lights incident, the fire code has gotten stricter: now, at
most ten thousand lights are allowed. You arrange them in a 100x100 grid.

Never one to let you down, Santa again mails you instructions on the ideal
lighting configuration. With so few lights, he says, you'll have to resort to
animation.

Start by setting your lights to the included initial configuration (your puzzle
input). A `#` means "on", and a `.` means "off".

Then, animate your grid in steps, where each step decides the next
configuration based on the current one. Each light's next state (either on or
off) depends on its current state and the current states of the eight lights
adjacent to it (including diagonals). Lights on the edge of the grid might have
fewer than eight neighbors; the missing ones always count as "off".

For example, in a simplified 6x6 grid, the light marked `A` has the neighbors
numbered `1` through `8`, and the light marked `B`, which is on an edge, only
has the neighbors marked `1` through `5`:

```
1B5...
234...
......
..123.
..8A4.
..765.
```

The state a light should have next is based on its current state (on or off)
plus the number of neighbors that are on:

- A light which is on stays on when `2` or `3` neighbors are on, and turns off
    otherwise.
- A light which is off turns on if exactly `3` neighbors are on, and stays off
    otherwise.

All of the lights update simultaneously; they all consider the same current
state before moving to the next.

Here's a few steps from an example configuration of another 6x6 grid:

```
Initial state:
.#.#.#
...##.
#....#
..#...
#.#..#
####..

After 1 step:
..##..
..##.#
...##.
......
#.....
#.##..

After 2 steps:
..###.
......
..###.
......
.#....
.#....

After 3 steps:
...#..
......
...#..
..##..
......
......

After 4 steps:
......
......
..##..
..##..
......
......
```

After `4` steps, this example has four lights on.

In your grid of 100x100 lights, given your initial configuration, how many
lights are on after 100 steps?

Part Two
========

You flip the instructions over; Santa goes on to point out that this is all
just an implementation of Conway's Game of Life. At least, it was, until you
notice that something's wrong with the grid of lights you bought: four lights,
one in each corner, are stuck on and can't be turned off. The example above
will actually run like this:

```
Initial state:
##.#.#
...##.
#....#
..#...
#.#..#
####.#

After 1 step:
#.##.#
####.#
...##.
......
#...#.
#.####

After 2 steps:
#..#.#
#....#
.#.##.
...##.
.#..##
##.###

After 3 steps:
#...##
####.#
..##.#
......
##....
####.#

After 4 steps:
#.####
#....#
...#..
.##...
#.....
#.#..#

After 5 steps:
##.###
.##..#
.##...
.##...
#.#...
##...#
```

After `5` steps, this example now has `17` lights on.

In your grid of 100x100 lights, given your initial configuration, but with the
four corners always in the on state, how many lights are on after 100 steps?
"""

from typing import MutableSequence

from aocd import get_data

DATA = get_data(year=2015, day=18)


class LightGrid:
    """Light Grid model."""

    def __init__(
        self, grid: MutableSequence[MutableSequence[int]], *, corners_on: bool = False
    ) -> None:
        """Initialize the LightGrid.

        :param grid: The initial state of the grid.
        :param corners_on: Force the corners to always be on after each step.
        """
        self.grid = grid
        self.corners_on = corners_on
        self._check_corners()

    def __str__(self) -> str:
        """String representation."""
        return "\n".join(
            "".join("#" if val else "." for val in line) for line in self.grid
        )

    def animate(self) -> "LightGrid":
        """Animate the grid to the next step."""
        grid_size = len(self.grid), len(self.grid[0])
        new_grid = []
        for i, line in enumerate(self.grid):
            new_line = []
            for j, val in enumerate(line):
                neighbors = 0
                for ni in range(max(0, i - 1), min(grid_size[0], i + 2)):
                    for nj in range(max(0, j - 1), min(grid_size[1], j + 2)):
                        if ni == i and nj == j:
                            continue
                        if self.grid[ni][nj]:
                            neighbors += 1

                if val and neighbors not in (2, 3):
                    val = 0
                elif not val and neighbors == 3:
                    val = 1

                new_line.append(val)

            new_grid.append(new_line)

        return LightGrid(new_grid, corners_on=self.corners_on)

    def _check_corners(self) -> None:
        """Ensure the state of the corners is expected."""
        if not self.corners_on:
            return

        grid_size = len(self.grid), len(self.grid[0])
        self.grid[0][0] = 1
        self.grid[0][grid_size[1] - 1] = 1
        self.grid[grid_size[0] - 1][0] = 1
        self.grid[grid_size[0] - 1][grid_size[1] - 1] = 1

    @property
    def lit(self) -> int:
        """Return the number of lit lights."""
        return sum(sum(line) for line in self.grid)

    @classmethod
    def from_text(cls, text: str, *, corners_on: bool = False) -> "LightGrid":
        """Create a light grid from a text string.

        :param text: The text string.
        """
        grid = [[1 if char == "#" else 0 for char in line] for line in text.split("\n")]
        return cls(grid, corners_on=corners_on)


def _run_animation(
    data: str = DATA, iterations: int = 100, corners_on: bool = False
) -> int:
    """Solve part 1.

    :param data: The input data.
    :param iterations: The number of times to animate the lights.
    """
    grid = LightGrid.from_text(data, corners_on=corners_on)
    for _ in range(iterations):
        grid = grid.animate()

    return grid.lit


def part1(data: str = DATA, iterations: int = 100) -> int:
    """Solve part 1.

    :param data: The input data.
    :param iterations: The number of times to animate the lights.
    """
    return _run_animation(data, iterations)


def part2(data: str = DATA, iterations: int = 100) -> int:
    """Solve part 1.

    :param data: The input data.
    :param iterations: The number of times to animate the lights.
    """
    return _run_animation(data, iterations, corners_on=True)
