from typing import Dict, List, Tuple

Join = Tuple[str, str]

class Polymer:
    def __init__(self, template: str) -> None:
        self.pairs: Dict[str, int] = {}
        self._add_pairs(template)

        self.counts: Dict[str, int] = {c: template.count(c) for c in set(template)}

    def __str__(self) -> str:
        return str(self.counts) + "\n" + str(self.pairs)

    def insert(self, joins: List[Join]) -> None:
        news: Dict[str, List[str, int]] = {}
        for join in joins:
            pair, add = join
            if pair in self.pairs and self.pairs[pair] > 0:
                n = self.pairs[pair]
                self._increment(add, n)
                if pair not in news: 
                    news[pair] = [pair[0] + add + pair[1], n]
                else:
                    news[pair][0] = pair[:-1] + add + pair[-1]
                    news[pair][1] += n
        for initial_pair, [new_template, times] in news.items():
            self._remove_pair(initial_pair, times)
            self._add_pairs(new_template, times)

    def commons(self) -> Tuple[int, int]:
        most = max(self.counts.values())
        least = min(self.counts.values())
        return least, most
    
    def _increment(self, c: str, count: int = 1) -> None:
        if c not in self.counts:
            self.counts[c] = count
        else:
            self.counts[c] += count
    
    def _add_pair(self, pair: str, count: int = 1) -> None:
        if pair not in self.pairs:
            self.pairs[pair] = count
        else: self.pairs[pair] += count
    
    def _remove_pair(self, pair: str, count: int = 1) -> None:
        if pair not in self.pairs or self.pairs[pair] - count < 0:
            raise Exception("Tried to remove a pair that doesn't exist or don't have enough of")
        self.pairs[pair] -= count
    
    def _add_pairs(self, template: str, count: int = 1) -> None:
        for i in range(1, len(template)):
            self._add_pair(template[i-1] + template[i], count)

def solve(filename: str = "input", steps: Tuple[int, int] = (10, 40)) -> Tuple[int, int]:
    polymer = Polymer("")
    joins: List[Join] = []
    with open(f"day14/{filename}", 'r') as f:
        while line := f.readline().strip():  # Template
            polymer = Polymer(line)
        while line := f.readline().strip():  # Joins
            join = (pair, add) = [part.strip() for part in line.split("->")]
            joins.append(join)
    for _ in range(steps[0]):
        polymer.insert(joins)
    least1, most1 = polymer.commons()
    for _ in range(steps[1] - steps[0]):
        polymer.insert(joins)
    least2, most2 = polymer.commons()
    return most1 - least1, most2 - least2


print(solve())
