"""Tests for AOC 2015-19."""

from dataclasses import dataclass

import pytest

from .advent_2015_19 import part1, part2


@dataclass
class MoleculeParams:
    """Molecule fixture."""

    molecule: str
    replacmenets: int
    steps: int


@pytest.fixture(name="replacements")
def _replacements() -> str:
    return """
H => HO
H => OH
O => HH
e => H
e => O
    """.strip()


@pytest.fixture(name="data", params=[("HOH", 4, 3), ("HOHOHO", 7, 6)])
def _data(replacements: str, request: pytest.FixtureRequest) -> MoleculeParams:
    molecule, count, steps = request.param
    return MoleculeParams(f"{replacements}\n\n{molecule}", count, steps)


def test_part_1(data: MoleculeParams) -> None:
    """Test part 1."""
    assert part1(data.molecule) == data.replacmenets


def test_part_2(data: MoleculeParams) -> None:
    """Test part 2."""
    assert part2(data.molecule) == data.steps
