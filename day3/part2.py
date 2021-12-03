from typing import List
from binary_diagnostic import Byte, BitCounts

# I really didn't want to save the input to a list but here we are.
def get_input(filename: str = "input") -> List[Byte]:
    bytes = []
    with open(f"day3/{filename}", 'r') as f:
        while line := f.readline().strip():
            bytes.append(Byte([int(i) for i in line]))
    return bytes

def get_oxygen_rating(bytes: List[Byte]) -> Byte:
    return get_rating(bytes, True)

def get_co2_rating(bytes: List[Byte]) -> Byte:
    return get_rating(bytes, False)

def get_rating(bytes: List[Byte], oxygen: bool = True):
    temp = bytes.copy()
    n = len(temp[0])
    i = 0
    while len(temp) > 1 and i != n:
        counts = BitCounts(n)
        for byte in temp:
            counts.add_byte(byte)
        rate = counts.get_gamma_rate() if oxygen else counts.get_epsilon_rate()
        temp = list(filter(lambda byte: byte[i] == rate[i], temp))
        i += 1
    return temp[0]

def solve(filename: str = "input") -> int:
    bytes = get_input(filename)
    oxygen_rating = get_oxygen_rating(bytes)
    co2_rating = get_co2_rating(bytes)
    return oxygen_rating.as_int() * co2_rating.as_int()

if __name__ == "__main__":
    result = solve()
    print(f"oxygen co2 rating product is {result}")
