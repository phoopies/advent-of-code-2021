from typing import Dict, List, Tuple

Join = Tuple[str, str]


class Polymer:
    def __init__(self, template: str) -> None:
        self.template = template
        self.temp = template

    def __str__(self) -> str:
        return self.template

    def insert(self, joins: List[Join]) -> None:
        joins_i: Dict[int, str] = {}
        for join in joins:
            pair, add = join
            i = self.template.find(pair)
            while i != -1:
                if i not in joins:
                    joins_i[i] = add
                else:
                    joins_i[i] += add
                i = self.template.find(pair, i+1)
        for i in sorted(joins_i.keys(), reverse=True):
            self.template = self.template[:(
                i+1)] + joins_i[i] + self.template[(i+1):]

    def commons(self) -> Tuple[Tuple[str, int], Tuple[str, int]]:
        most = max(self.template, key=self.template.count)
        least = min(self.template, key=self.template.count)
        return (least, self.template.count(least)), (most, self.template.count(most))


def solve(filename: str = "input", steps: int = 10) -> Tuple[int, int]:
    polymer = Polymer("")
    joins: List[Join] = []
    with open(f"day14/{filename}", 'r') as f:
        while line := f.readline().strip():  # Template
            polymer = Polymer(line)
        while line := f.readline().strip():  # Joins
            join = (pair, add) = [part.strip() for part in line.split("->")]
            joins.append(join)
    for _ in range(steps):
        polymer.insert(joins)
    (_l, lc), (_m, mc) = polymer.commons()
    return mc - lc


print(solve())
