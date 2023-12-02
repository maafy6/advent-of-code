"""Tests for AOC 2015-07."""

import pytest

from .advent_2015_07 import CircuitBoard


@pytest.mark.asyncio
async def test_eval_circuit() -> None:
    """Test eval_circuit."""
    circuit = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
    """.strip()

    expected = {
        "d": 72,
        "e": 507,
        "f": 492,
        "g": 114,
        "h": 65412,
        "i": 65079,
        "x": 123,
        "y": 456,
    }

    board = CircuitBoard()
    await board.eval_circuit(circuit)

    for key, value in expected.items():
        assert board[key] == value
