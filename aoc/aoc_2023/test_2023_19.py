"""Tests for AOC 2023-19."""

from textwrap import dedent

import pytest

from .advent_2023_19 import Part, Workflow, WorkflowCondition, part1, part2


@pytest.fixture(name="data")
def _data() -> str:
    return dedent(
        """
            px{a<2006:qkq,m>2090:A,rfg}
            pv{a>1716:R,A}
            lnx{m>1548:A,A}
            rfg{s<537:gd,x>2440:R,A}
            qs{s>3448:A,lnx}
            qkq{x<1416:A,crn}
            crn{x>2662:A,R}
            in{s<1351:px,qqz}
            qqz{s>2770:qs,m<1801:hdj,R}
            gd{a>3333:R,R}
            hdj{m>838:A,pv}

            {x=787,m=2655,a=1222,s=2876}
            {x=1679,m=44,a=2067,s=496}
            {x=2036,m=264,a=79,s=2244}
            {x=2461,m=1339,a=466,s=291}
            {x=2127,m=1623,a=2188,s=1013}
        """
    ).strip()


@pytest.fixture(name="workflow")
def _workflow() -> Workflow:
    return Workflow(
        "in",
        [
            WorkflowCondition("s", "<", 1351, "px"),
            WorkflowCondition(None, None, None, "qqz"),
        ],
    )


@pytest.mark.parametrize(
    ("fields", "score"),
    [
        ({"x": 787, "m": 2655, "a": 1222, "s": 2876}, 7540),
        ({"x": 2036, "m": 264, "a": 79, "s": 2244}, 4623),
        ({"x": 2127, "m": 1623, "a": 2188, "s": 1013}, 6951),
    ],
)
def test_score(fields: dict[str, int], score: int) -> None:
    """Test score"""
    assert Part(**fields).score == score


@pytest.mark.parametrize(
    ("part", "output"),
    [
        (Part(787, 2655, 1222, 2876), "qqz"),
        (Part(1679, 44, 2067, 496), "px"),
    ],
)
def test_apply_workflow(part: Part, output: str, workflow: Workflow) -> None:
    """Test apply workflow."""
    assert workflow.apply(part) == output


def test_part_1(data: str) -> None:
    """Test Part 1."""
    assert part1(data) == 19114


def test_part_2(data: str) -> None:
    """Test Part 2."""
    assert part2(data) == 167409079868000
