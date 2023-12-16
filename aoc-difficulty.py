#! /usr/bin/env python
# coding: utf-8

from dataclasses import dataclass
import sys
from typing import Optional

import bs4
import httpx


@dataclass
class DayStat:
    day: int
    silver: int
    gold: int

    def __post_init__(self):
        self.day = int(self.day)
        self.silver = int(self.silver)
        self.gold = int(self.gold)
        self.participants = self.silver + self.gold
        self.rel_gold = self.gold * 100.0 / self.participants

    @staticmethod
    def hdr(title: str = ""):
        print(title.upper(), end="\n\n")
        print("Day    Solved both parts    Participants")
        print("---    -----------------    ------------")

    def __str__(self):
        return f"{self.day:3}  {self.rel_gold:>18.2f}%  {self.gold + self.silver:>14,}"


def retrieve_stats(year: int) -> list[DayStat]:
    page = httpx.get(f"https://adventofcode.com/{year}/stats")
    soup = bs4.BeautifulSoup(page, "html.parser")

    def to_int(elem: bs4.element.Tag) -> int:
        try:
            return int(elem.contents[0])
        except (IndexError, ValueError):
            return -1

    silver: list[int] = [
        to_int(s) for s in soup.find_all("span", class_="stats-firstonly") if to_int(s) >= 0
    ]
    gold: list[int] = [
        to_int(s) for s in soup.find_all("span", class_="stats-both") if to_int(s) >= 0
    ]

    return [
        DayStat(day + 1, s, g)
        for day, (s, g) in enumerate(zip(silver[::-1], gold[::-1]))
        if s + g > 0
    ]


def print_stats(year: int):
    stats = retrieve_stats(year)

    DayStat.hdr(f"{year} by day")
    for s in stats:
        print(s)

    print()
    DayStat.hdr(f"{year} by difficulty")
    for s in sorted(stats, key=lambda x: x.rel_gold):
        print(s)

    print()
    print(f"Total: {sum(s.participants for s in stats):,}")
    print("=" * 40, end="\n\n")


def main():
    if len(sys.argv) < 2:
        print_stats(2023)
    else:
        for year in [y + 2000 if y < 100 else y for y in map(int, sys.argv[1:])]:
            print_stats(year)


if __name__ == "__main__":
    main()
