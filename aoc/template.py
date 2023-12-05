"""Generate template files for AOC."""

import re
from textwrap import wrap
from typing import Optional

from aocd.get import current_day, default_user, most_recent_year
from aocd.models import Puzzle
from aocd.utils import http
from bs4 import BeautifulSoup, Tag


def fetch_puzzle(
    day: Optional[int] = None, year: Optional[int] = None
) -> BeautifulSoup:
    """Fetch the puzzle for the given date.

    :param day: The day to fetch.
    :param year: The year to fetch.
    """
    user = default_user()

    if day is None:
        day = current_day()

    if year is None:
        year = most_recent_year()

    puzzle = Puzzle(year=year, day=day, user=user)
    response = http.get(puzzle.url, token=puzzle.user.token)
    return BeautifulSoup(response.data, "html.parser")


def format_header(text: str) -> str:
    """Format the header text.

    :param text: The header text.
    :returns: The formatted text.
    """
    if match := re.match(r"--- (.*) ---", text):
        title = match.group(1)
        return f"{title}\n{'=' * len(title)}\n"

    return text


def format_text(elem: Tag) -> str:
    """Format the element text.

    :param elem: The element.
    :returns: The formatted text.
    """
    output = ""
    if elem.name == "li":
        output = "- "

    for child in elem.children:
        if isinstance(child, Tag) and child.name == "code":
            output += f"`{child.text}`"
        else:
            output += child.text

    return output


def get_description(day: Optional[int] = None, year: Optional[int] = None) -> str:
    """Return the description for the day.

    :param day: The day of the puzzle.
    :param year: The year of the puzzle.
    :returns: The formatted puzzle description.
    """
    parser = fetch_puzzle(day, year)
    output = ""
    for part in parser.find_all("article"):
        for elem in part:
            if not isinstance(elem, Tag):
                continue

            if elem.name == "h2":
                output += format_header(elem.text)
                output += "\n"
            elif elem.name == "p":
                output += "\n".join(wrap(format_text(elem), width=80))
                output += "\n\n"
            elif elem.name == "ul":
                for li in elem.find_all("li"):
                    output += "\n".join(
                        wrap(format_text(li), width=80, subsequent_indent="    ")
                    )
                    output += "\n"
                output += "\n"
            elif elem.name == "pre":
                output += "```\n"
                output += elem.text
                output += "```\n"
                output += "\n"

    return output


def main_template(year: int, day: int) -> str:
    """Get the main template for the puzzle."""
    return f"""\"""Advent of Code {year}: Day {day}

{get_description(day=day, year=year)}\"""

from aocd import get_data

DATA = get_data(year={year}, day={day})


def part1(data: str = DATA) -> int:
    \"""Solve Part 1.

    :param data: The input data.
    :returns: The solution.
    \"""


def part2(data: str = DATA) -> int:
    \"""Solve Part 2.

    :param data: The input data.
    :returns: The solution.
    \"""
    """
