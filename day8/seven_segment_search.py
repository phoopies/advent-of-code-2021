from typing import List
from time import time
# PART 1

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

# PART 2
# Another solution to part 2. I prefer as it's easier to follow and it seems to be a bit faster which is nice.

# Another way to solve day 8 part 2. 
# We don't need to know which wire goes where but which number a combination represents.
# We can determine numbers 1 4 7 and 8 easily as they have a unique number of segments
# From here we can determine number 9 as it the only six segment number that shares same segments as number 4
# Same goes for number 0 (compare to 7)
# Same goes for number 3 (compare to 7, 5 segments) 
# The last six segment number must be number 6
# At this point we only need to determine numbers 2 and 5
# Compared to number 4, 5 has more segments in common than 2. We can use this to determine the last two numbers.

class Display:
    a: int = 97
    segments: int = 7
    unknown: str = "?"
    number_segments: List[int] = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6] # How many segments each number (index) has

    def __init__(self, patterns: List[str]) -> None:
        self.input = patterns
        self.patterns = [Display.unknown for _ in patterns]
        self.determine() 
    
    def to_number(self, pattern: str) -> int:
        for i, pat in enumerate(self.patterns):
            if pat == sorted(pattern): return i
        return -1
    
    def determine(self):
        self._determine_w_counts()
        self._determine_w_comparing(9, 4)
        self._determine_w_comparing(0, 7)
        self._determine_w_comparing(3, 7)
        self._determine_six()
        self._determine_two_and_five()
        self.patterns = [sorted(pattern) for pattern in self.patterns]
    
    def _determine_w_counts(self) -> None:
        to_determine = [1, 4, 7, 8] # could also get the unique ones from number_segments
        for t in to_determine:
            pattern = self._get_w_count(Display.number_segments[t])[0]
            self.patterns[t] = pattern
    
    def _determine_six(self) -> None:
        segments6 = self._get_w_count(6)
        for pattern in segments6:
            if pattern not in self.patterns:
                self.patterns[6] = pattern
                return

    def _determine_two_and_five(self) -> None:
        four = self.patterns[4]
        fst, snd = self._get_unsolved()
        in_common_fst = len(set(four).intersection(set(fst)))
        in_common_snd = len(set(four).intersection(set(snd)))
        if in_common_fst > in_common_snd: 
            self.patterns[5] = fst
            self.patterns[2] = snd
        else:
            self.patterns[5] = snd
            self.patterns[2] = fst
    
    def _get_unsolved(self) -> List[str]:
        unsolved = []
        for pattern in self.input:
            if pattern not in self.patterns:
                unsolved.append(pattern)
        return unsolved

    def _determine_w_comparing(self, to_determine: int, to_compare_with: int) -> None:
        segments = Display.number_segments[to_determine]
        compare = self.patterns[to_compare_with]
        possible_patterns = self._get_w_count(segments)
        for pattern in possible_patterns:
            if pattern in self.patterns: 
                continue
            correct = True
            for c in compare:
                if c not in pattern:
                    correct = False
                    break
            if correct:
                self.patterns[to_determine] = pattern
                return


    def _get_w_count(self, n:int) -> List[str]:
        return list(filter(lambda p: len(p) == n, self.input))

def solve(filename: str = "input"):
    s = 0
    with open(f"day8/{filename}", 'r') as f:
        while line := f.readline().strip():
            patterns, outputs = [l.strip().split(' ') for l in line.split('|')]
            display = Display(patterns)
            value = ""
            for output in outputs:
                value += str(display.to_number(output))
            s += int(value)
    return s
        
print(solve())        

start = time()
for _ in range(1000):
    solve()
end = time()
print(f"Took {end-start} seconds") # about 5.8 seconds