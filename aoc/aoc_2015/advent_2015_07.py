"""Advent of Code 2015 - Day 7

Day 7: Some Assembly Required
=============================

This year, Santa brought little Bobby Tables a set of wires and bitwise logic
gates! Unfortunately, little Bobby is a little under the recommended age range,
and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit
signal (a number from `0` to `65535`). A signal is provided to each wire by a
gate, another wire, or some specific value. Each wire can only get a signal
from one source, but can provide its signal to multiple destinations. A gate
provides no signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts together:
`x AND y -> z` means to connect wires `x` and `y` to an `AND` gate, and then
connect its output to wire `z`.

For example:

- `123 -> x` means that the signal `123` is provided to wire `x`.
- `x AND y -> z` means that the bitwise AND of wire `x` and wire `y` is
    provided to wire `z`.
- `p LSHIFT 2 -> q` means that the value from wire `p` is left-shifted by `2`
    and then provided to wire `q`.
- `NOT e -> f` means that the bitwise complement of the value from wire `e` is
    provided to wire `f`.

Other possible gates include `OR` (bitwise OR) and `RSHIFT` (right-shift). If,
for some reason, you'd like to emulate the circuit instead, almost all
programming languages (for example, C, JavaScript, or Python) provide operators
for these gates.

For example, here is a simple circuit:

```
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
```

After it is run, these are the signals on the wires:

```
d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456
```

In little Bobby's kit's instructions booklet (provided as your puzzle input),
what signal is ultimately provided to wire `a`?

Part Two
========

Now, take the signal you got on wire `a`, override wire `b` to that signal, and
reset the other wires (including wire `a`). What new signal is ultimately
provided to wire `a`?
"""

import asyncio
import re
from typing import Dict, Union

from aocd import get_data

DATA = get_data(year=2015, day=7)

WireOrValue = Union[str, int]


class CircuitBoard:
    """Circuit board emulator."""

    def __init__(self):
        self._circuits: Dict[str, asyncio.Future] = {}

    async def eval_circuit(self, data: str) -> None:
        """Evaluate a circuit based on the instructions.

        This method will await until all instructions have been completed. If
        the circuit board is incomplete, this will hang forever.

        :param data: The input instructions.
        """
        tasks = []
        for line in data.split("\n"):
            if match := re.match(r"(.*)->(.*)", line):
                instruction, target = match.group(1).strip(), match.group(2).strip()
                task = asyncio.create_task(self.apply_instruction(instruction, target))
                tasks.append(task)

        await asyncio.gather(*tasks)

    async def apply_instruction(self, instruction: str, target: str) -> None:
        """Apply the instruction to the circuit board.

        :param instruction: The instruction to apply.
        :param target: The target wire to receive the output of the instruction.
        """
        if match := re.match(r"NOT (.*)", instruction):
            self[target] = await self.bitnot(match.group(1).strip())
        elif match := re.match(r"(.*) LSHIFT (.*)", instruction):
            self[target] = await self.lshift(
                match.group(1).strip(), match.group(2).strip()
            )
        elif match := re.match(r"(.*) RSHIFT (.*)", instruction):
            self[target] = await self.rshift(
                match.group(1).strip(), match.group(2).strip()
            )
        elif match := re.match(r"(.*) AND (.*)", instruction):
            self[target] = await self.bitand(
                match.group(1).strip(), match.group(2).strip()
            )
        elif match := re.match(r"(.*) OR (.*)", instruction):
            self[target] = await self.bitor(
                match.group(1).strip(), match.group(2).strip()
            )
        else:
            await self.set(target, instruction)

    async def get(self, key: str) -> int:
        """Get the item value.

        :param key: The wire ID.
        :returns: The value of the wire.
        """
        if key not in self._circuits:
            self._circuits[key] = asyncio.Future()

        return await self._circuits[key]

    async def set(self, key: str, value: str) -> int:
        """Set the item value.

        :param key: The wire ID.
        :param value: The value to set.
            If the value is a wire ID, it will await the value of that wire to
            be set, else the value will be interpreted as an integer and set
            immediately.
        :returns: The value set.
        """
        if (key not in self._circuits) or self._circuits[key].done():
            self._circuits[key] = asyncio.Future()

        try:
            value = int(value)
        except ValueError:
            value = await self.get(value)

        self._circuits[key].set_result(value)
        return value

    def __getitem__(self, key: str) -> int:
        """Return the value of the wire.

        :param key: The wire ID.
        :returns: The value of the wire.
        """
        return self._circuits[key].result()

    def __setitem__(self, key: str, value: int) -> int:
        """Set the item value as a future.

        :param key: The wire ID.
        :param value: The wire value.
        :returns: The value of the wire.
        """
        if key not in self._circuits:
            self._circuits[key] = asyncio.Future()

        self._circuits[key].set_result(value)
        return value

    async def bitand(self, input1: WireOrValue, input2: WireOrValue) -> int:
        """Bitwise AND.

        If `input1` or `input2` are wire IDs, the values of those wires will be
        awaited before completing.

        :param input1: The first input.
        :param input2: The second input.
        :returns: The bitwise AND of the two inputs.
        """
        try:
            input1 = int(input1)
        except ValueError:
            input1 = await self.get(input1)

        try:
            input2 = int(input2)
        except ValueError:
            input2 = await self.get(input2)

        return input1 & input2

    async def bitor(self, input1: WireOrValue, input2: WireOrValue) -> int:
        """Bitwise OR.

        If `input1` or `input2` are wire IDs, the values of those wires will be
        awaited before completing.

        :param input1: The first input.
        :param input2: The second input.
        :returns: The bitwise OR of the two inputs.
        """
        try:
            input1 = int(input1)
        except ValueError:
            input1 = await self.get(input1)

        try:
            input2 = int(input2)
        except ValueError:
            input2 = await self.get(input2)

        return input1 | input2

    async def lshift(self, value: WireOrValue, shift: int) -> int:
        """Bitshift left.

        If `value` is a wire ID, the values of those wires will be awaited
        before completing.

        :param value: The input value.
        :param shift: The number of spaces to shift.
        :returns: The shifted output of the value masked to 16 bits.
        """
        try:
            value = int(value)
        except ValueError:
            value = await self.get(value)

        try:
            shift = int(shift)
        except ValueError:
            shift = await self.get(shift)

        return (value << shift) & 0xFFFF

    async def rshift(self, value: Union[str, int], shift: int) -> int:
        """Bitshift right.

        If `value` is a wire ID, the values of those wires will be awaited
        before completing.

        :param value: The input value.
        :param shift: The number of spaces to shift.
        :returns: The shifted output of the value masked to 16 bits.
        """
        try:
            value = int(value)
        except ValueError:
            value = await self.get(value)

        try:
            shift = int(shift)
        except ValueError:
            shift = await self.get(shift)

        return (value >> shift) & 0xFFFF

    async def bitnot(self, value: WireOrValue) -> int:
        """Bitwise NOT.

        If `value` is a wire ID, the values of those wires will be awaited
        before completing.

        :param value: The input value.
        :returns: The 16-bit complement of the value.
        """
        try:
            value = int(value)
        except ValueError:
            value = await self.get(value)

        return value ^ 0xFFFF


async def part1(data: str = DATA) -> int:
    """Calculate part 1.

    :param data: The input data.
    :returns: The value of circuit a.
    """
    board = CircuitBoard()
    await board.eval_circuit(data)

    return board["a"]


async def part2(data: str = DATA) -> int:
    """Calculate part 2.

    :param data: The input data.
    :returns: The value of circuit a.
    """
    b_override = await part1(data)

    new_data = []
    for line in data.split("\n"):
        if line.endswith("-> b"):
            new_data.append(f"{b_override} -> b")
        else:
            new_data.append(line)

    board = CircuitBoard()
    await board.eval_circuit("\n".join(new_data))

    return board["a"]
