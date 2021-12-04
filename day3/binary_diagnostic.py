from enum import Enum
from typing import List, Tuple, Union

class Bit(Enum):
    ZERO = 0
    ONE = 1

    def __str__(self) -> str:
        return str(self.value)

    def inverted(self):
        if self is Bit.ZERO: return Bit.ONE
        else: return Bit.ZERO

class Byte:
    def __init__(self, bits: Union[List[Bit], List[int]] = []) -> None:
        self.byte = bits if all(isinstance(bit, Bit) for bit in bits) else [Bit(i) for i in bits]
    
    def __str__(self) -> str:
        return "".join([str(bit) for bit in self.byte])
    
    def __setitem__(self, key:int, value: Bit):
        self.byte[key] = value
    
    def __getitem__(self, key:int):
        return self.byte[key]
    
    def __len__(self) -> int:
        return len(self.byte)
    
    def inverted(self):
        byte = self.byte.copy()
        for i in range(len(byte)):
            byte[i] = byte[i].inverted()
        return Byte(byte)
    
    def as_int(self) -> int:
        n = len(self.byte)  - 1
        i = 0
        for bit in self.byte:
            i += bit.value * 2**n
            n -= 1
        return i
    
    def append(self, bit: Bit):
        if not isinstance(bit, Bit): raise Exception("Value is not type of Bit")
        self.byte.append(bit)

class BitCount:
    def __init__(self) -> None:
        self.zeros = 0
        self.ones = 0
    
    def __str__(self) -> str:
        return f"Zeros: {self.zeros}\tOnes:{self.ones}"

    def add(self, b: Bit) -> None:
        if b is Bit.ZERO: self.zeros += 1
        else: self.ones += 1
    
    def add_str(self, s:str) -> None:
        if not s.isdigit(): return
        i = int(s)
        if i not in [0,1]: return
        self.add(Bit(i))
    
    def most_common(self, default:int = 1) -> Bit:
        if self.zeros == self.ones: return Bit(default)
        return Bit(self.zeros < self.ones)

class BitCounts:
    def __init__(self, n: int) -> None:
        self.counts = [BitCount() for _ in range(n)]
        default = BitCount().most_common()
        self.gamma_rate: Byte = Byte([default] *n)
        self.epsilon_rate: Byte = Byte([Bit(not default)] * n)
        self.dirty = False
    
    def __str__(self) -> str:
        self.get_gamma_rate()
        return (
            "zeros: " + "".join([f'{count.zeros} ' for count in self.counts]) +
            "\nones: " + "".join([f'{count.ones} ' for count in self.counts]) +
            f"\ngamma rate: {str(self.gamma_rate)}={self.gamma_rate.as_int()}"
            f"\nepsilon rate: {str(self.epsilon_rate)}={self.epsilon_rate.as_int()}"
        )
    
    def add(self, i:int, bit:Bit):
        self.counts[i].add(bit)
        self.dirty = True
    
    def add_byte(self, byte: Byte):
        if len(byte) > len(self.counts): return
        for i, bit in enumerate(byte): self.add(i, bit)
    
    def add_str(self, s:str):
        if len(s) > len(self.counts): return
        for i, c in enumerate(s):
            self.counts[i].add_str(c)
        self.dirty = True
    
    def get_gamma_rate(self) -> Byte:
        if not self.dirty: return self.gamma_rate
        for i, count in enumerate(self.counts):
            self.gamma_rate[i] = count.most_common()
        self.epsilon_rate = self.gamma_rate.inverted()
        self.dirty = False
        return self.gamma_rate

    def get_epsilon_rate(self) -> Byte:
        if not self.dirty: return self.epsilon_rate
        self.get_gamma_rate()
        return self.epsilon_rate
        

def solve(filename: str = "input") -> Tuple[int, BitCounts]:
    with open(f"day3/{filename}", 'r') as f:
        line = f.readline().strip()
        counts = BitCounts(len(line))
        counts.add_str(line)
        while line := f.readline().strip():
            counts.add_str(line)
    return counts.get_gamma_rate().as_int() * counts.get_epsilon_rate().as_int(), counts

if __name__ == "__main__":
    result, counts = solve()

    print(str(counts))
    print(f"Delta epsilon product is {result}")
