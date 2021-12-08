from enum import Enum
from typing import List, Union

# print(
#     len([e for row in list(
#         map(lambda l: list(filter(lambda e: len(e) in [2, 3, 4, 7], l)),
#             map(lambda l: l.split(' '),
#                 map(lambda l: l.split('|')[1],
#                 [line.strip() for line in open("day8/input")]
#                 )
#             )
#        )
#     ) for e in row])
# )

class Segment(object):
    count_relations = {
        4 : 'e',
        6 : 'b',
        9 : 'f',
        7 : ['d', 'g'],
        8 : ['a', 'c'],
    }
    unknown = "?"

    def __init__(self) -> None:
        self.count = 0
        self._real = Segment.unknown
        self.solved = False

    @property
    def real(self) -> Union[str, List[str]]:
        return self._real

    @real.setter
    def real(self, s:Union[str, List[str]]) -> None:
        if isinstance(s, str) and s != Segment.unknown: self.solved = True
        else: self.solved = False
        self._real = s
    
    def __str__(self) -> str:
        return f"{self.real} ({self.count}) ({self.solved})"
    
    def __add__(self, o: int) -> None:
        self.count += o
        self._update_w_count()
    
    def _update_w_count(self) -> None:
        if self.count in Segment.count_relations.keys():
            self.real = Segment.count_relations[self.count]
        


class Display:
    correct = {
        'abcefg': 0,
        'cf' : 1,
        'acdeg' : 2,
        'acdfg' : 3,
        'bcdf' : 4,
        'abdfg' : 5,
        'abdefg' : 6,
        'acf' : 7,
        'abcdefg' : 8,
        'abcdfg' : 9
    }
    a: int = 97
    segments: int = 7
    def __init__(self, patterns: List[str]) -> None:
        self.patterns = patterns
        self.numbers = {chr(i + Display.a):Segment() for i in range(Display.segments)}
        self.determine()
    
    def to_number(self, pattern: str) -> int:
        s = "".join(sorted([self.numbers[wire].real for wire in pattern]))
        return Display.correct[s]
    
    def determine(self):
        self._determine_counts()
        self._determine_c()
        self._determine_a()
        self._determine_d()
        self._determine_g()
    
    def _determine_counts(self) -> None:
        for pattern in self.patterns:
            for c in pattern:
                self.numbers[c] + 1

    def _determine_c(self):
        n_one = self._get_w_length(2)
        for wire in n_one:
            if not self.numbers[wire].solved: 
                if 'c' in self.numbers[wire].real: self.numbers[wire].real = 'c'
                else: self.numbers[wire].real = 'f'
                return
    
    def _determine_a(self):
        n_one = self._get_w_length(2)
        n_seven = self._get_w_length(3)
        for wire in n_seven:
            if wire not in n_one: 
                self.numbers[wire].real = 'a'
                return
    
    def _determine_d(self): 
        n_four = self._get_w_length(4)
        for wire in n_four: 
            if not self.numbers[wire].solved:
                self.numbers[wire].real = 'd'
                return
    
    def _determine_g(self):
        for segment in self.numbers.values():
            if not segment.solved: 
                segment.real = 'g'
                return

    def _get_w_length(self, n:int) -> str:
        return list(filter(lambda p: len(p) == n, self.patterns))[0]

def solve(filename: str = "input"):
    s = 0
    with open(f"day8/{filename}", 'r') as f:
        while line := f.readline().strip():
            patterns, outputs = [l.split(' ') for l in line.split('|')]
            display = Display(patterns)
            value = ""
            for output in outputs:
                if output == "": continue
                value += str(display.to_number(output))
            s += int(value)
    return s
        

print(solve())

