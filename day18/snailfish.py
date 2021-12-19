from typing import List, Tuple, Union
from math import floor, ceil
import json
from copy import deepcopy

class SnailfishNumber:
    def __init__(self) -> None:
        self.parent: 'SnailfishNumber' = None

    def set_parent(self, parent: 'SnailfishNumber') -> None:
        self.parent = parent

    def __add__(self, number: 'SnailfishNumber') -> 'SnailfishNumber':
        return SnailfishPair(self, number)


class SnailfishRegular(SnailfishNumber):
    def __init__(self, number: int) -> None:
        super().__init__()
        self.number = number

    def __str__(self) -> str:
        return str(self.number)

    def explode(self, deep: int, left: bool = False) -> bool:
        return False

    def split(self, left: bool) -> bool:
        if self.number > 9:
            div = self.number/2
            new = SnailfishPair(floor(div), ceil(div))
            if left:
                self.parent.left = new
            else:
                self.parent.right = new
            new.set_parent(self.parent)
            return True
        return False

    def get_right_regular(self) -> 'SnailfishRegular':
        return self

    def get_left_regular(self) -> 'SnailfishRegular':
        return self

    def magnitude(self) -> int:
        return self.number

class SnailfishPair(SnailfishNumber):
    def __init__(self, left: Union[SnailfishNumber, int], right: Union[SnailfishNumber, int]) -> None:
        super().__init__()
        if isinstance(left, int):
            left = SnailfishRegular(left)
        left.set_parent(self)
        self.left = left

        if isinstance(right, int):
            right = SnailfishRegular(right)
        right.set_parent(self)
        self.right = right

    def get_right_regular(self) -> SnailfishRegular:
        return self.right.get_right_regular()

    def get_left_regular(self) -> SnailfishRegular:
        return self.left.get_left_regular()

    def explode(self, deep: int = 0, from_left: bool = False) -> bool:
        if deep >= 4: 
            parentl = self.parent
            left = None
            while parentl is not None and parentl.get_left_regular() == self.left:
                parentl = parentl.parent
            if parentl != None:       
                left = parentl.left.get_right_regular()

            parentr = self.parent
            right = None
            while parentr is not None and parentr.get_right_regular() == self.right:
                parentr = parentr.parent
            if parentr != None:       
                right = parentr.right.get_left_regular()
            if left != None:
                left.number += self.left.number
            if right != None:
                right.number += self.right.number
            new = SnailfishRegular(0)
            new.set_parent(self.parent)
            if from_left:
                self.parent.left = new
            else:
                self.parent.right = new
            return True
        if isinstance(self, SnailfishPair):
            return self.left.explode(deep+1, True) or self.right.explode(deep+1, False)
        return False

    def split(self, left: bool = False) -> bool:
        return self.left.split(True) or self.right.split(False)

    def reduce(self) -> None:
        while self.explode():
            pass
        if self.split():
            self.reduce()
    
    def magnitude(self) -> int:
        return 3*(self.left.magnitude()) + 2 *self.right.magnitude()

    def __str__(self) -> str:
        return f"[{str(self.left)}, {str(self.right)}]"


def create_snailfish(ls) -> SnailfishNumber:
    if isinstance(ls, int): return SnailfishRegular(ls)
    return SnailfishPair(create_snailfish(ls[0]), create_snailfish(ls[1]))


def solve(filename: str = "input") -> Tuple[int, int]:
    sfs: List[SnailfishNumber] = []
    with open(f"day18/{filename}", 'r') as f:
        while line := f.readline().strip():
            sfs.append(create_snailfish(json.loads(line)))
    
    largest = 0
    for x, sf1 in enumerate(sfs):
        for y, sf2 in enumerate(sfs):
            if x == y: continue
            sf1_c = deepcopy(sf1)
            sf2_c = deepcopy(sf2)
            sf = (sf1_c+sf2_c)
            sf.reduce()
            mag = sf.magnitude()
            largest = max(largest, mag)

    sf = deepcopy(sfs[0])
    for sfn in sfs[1:]:
        sfn_c = deepcopy(sfn)
        sf = sf + sfn_c
        sf.reduce()

    return sf.magnitude(), largest

if __name__ == "__main__":
    testing = True
    if testing:
        s1 = SnailfishPair(1, 2)
        s2 = SnailfishPair(SnailfishPair(3, 4), 5)
        s3 = SnailfishPair(9, SnailfishPair(8, 7))
        s4 = SnailfishPair(s2, s3)

        sf1 = SnailfishPair(
            SnailfishPair(
                SnailfishPair(
                    SnailfishPair(4, 3), 4
                ), 4
            ),
            SnailfishPair(
                7, SnailfishPair(
                    SnailfishPair(8, 4), 9
                )
            )
        )

        sf2 = SnailfishPair(1, 1)
        sf3 = sf1 + sf2
        sf3.reduce()
        print(sf3)

        sf4 = SnailfishPair(
            SnailfishPair(1,2),
            SnailfishPair(
                SnailfishPair(3,4),5
            )
        )

        print(sf4.magnitude())

        sf5 = create_snailfish([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
        print(sf5.magnitude())

        print(solve("test_data"))
    print(solve())
