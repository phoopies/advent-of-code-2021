from functools import reduce
from typing import List, Literal, Tuple
from enum import Enum


class PacketType(Enum):
    operator = 1
    literal = 4


class LengthType(Enum):
    bits = '0'
    number = '1'


class Packet:
    def __init__(self, version: int, type_id: int, length: int) -> None:
        self.version = version
        self.type_id = type_id
        self.length = length

    def __str__(self) -> str:
        return f"\nversion: {self.version}\ntype_id: {self.type_id}\nlength: {self.length}"

    def version_sum(self) -> int:
        return self.version

    # Abstract method
    def value(self) -> int:
        return 0


class LiteralPacket(Packet):
    def __init__(self, version: int, type_id: int, length: int, literal: int) -> None:
        super().__init__(version, type_id, length)
        self.literal = literal

    def __str__(self) -> str:
        return super().__str__() + f"\nliteral: {self.literal}\n"

    def value(self) -> int:
        return self.literal


class OperatorPacket(Packet):
    def __init__(self, version: int, type_id: int, length: int) -> None:
        super().__init__(version, type_id, length)
        self.packets: List[Packet] = []

    def __str__(self) -> str:
        return super().__str__() + "\n" + "\n".join(["\t"*i + str(sub_packet) for i, sub_packet in enumerate(self.packets)])

    def add_sub_packet(self, packet: Packet) -> None:
        self.packets.append(packet)
        self.length += packet.length

    def version_sum(self) -> int:
        return reduce(lambda a, b: a+b, [sp.version_sum() for sp in self.packets], super().version_sum())

    def value(self) -> int:
        sb_values = [sb.value() for sb in self.packets]
        t = [sum, lambda x: reduce(lambda a, b: a*b, x, 1), min, max, None, lambda x: int(
            x[0] > x[1]), lambda x: int(x[0] < x[1]), lambda x: int(x[0] == x[1])]
        return t[self.type_id](sb_values)


class Decoder:
    data = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111'
    }

    length_type_id = {
        LengthType.bits: 15,
        LengthType.number: 11,
    }

    def __init__(self) -> None:
        pass

    def decode(self, data: str) -> Tuple[Packet, str]:
        b = self.hex_to_bin(data)
        return self.decode_b(b)

    def decode_b(self, bdata: str) -> Tuple[Packet, str]:
        version, s = self._get_version(bdata)
        type_id, s = self._get_type_id(s)
        if type_id == PacketType.literal.value:
            literal, n = self._get_literal(s)
            return LiteralPacket(version, type_id, n+6, literal), s[n:]
        opacket = OperatorPacket(version, type_id, 6)
        s = self._add_to_operator_packet(opacket, s)
        return opacket, s

    def hex_to_bin(self, data: str) -> str:
        return reduce(lambda b, hx: b + Decoder.data[hx], data, '')

    def bin_to_dec(self, b: str) -> int:
        n = len(b) - 1
        d = 0
        for i, c in enumerate(b):
            if c == '1':
                d += 2 ** (n-i)
        return d

    def _get_literal(self, s: str) -> Tuple[int, int]:
        bi = ""
        n = 0
        while s[0] != '0':
            b, s = self._split(s, 5)
            bi += b[1:]
            n += 5
        bi += s[1:5]
        return self.bin_to_dec(bi), n+5

    def _add_to_operator_packet(self, opacket: OperatorPacket, s: str) -> str:
        # if all([c == '0' for c in s]): return s
        length_type, s = self._get_length_type_id(s)
        n_sub, s = self._get_number_of_sub_packets(length_type, s)
        if length_type == LengthType.number:
            opacket.length += 12
            return self._add_to_operator_packet_n(opacket, s, n_sub)
        else:
            opacket.length += 16
            return self._add_to_operator_packet_b(opacket, s, n_sub)

    def _add_to_operator_packet_n(self, opacket: OperatorPacket, s: str, n: int) -> str:
        for _ in range(n):
            packet, s = self.decode_b(s)
            opacket.add_sub_packet(packet)
        return s

    def _add_to_operator_packet_b(self, opacket: OperatorPacket, s: str, bits: int) -> str:
        n = 0
        while n < bits:
            packet, s = self.decode_b(s)
            opacket.add_sub_packet(packet)
            n += packet.length
        return s

    def _get_version(self, s: str) -> Tuple[int, str]:
        return self._get_data(s, 3)

    def _get_length_type_id(self, s: str) -> Tuple[LengthType, str]:
        id, s = self._split(s, 1)
        return LengthType(id), s

    def _get_number_of_sub_packets(self, length_type: LengthType, s: str) -> Tuple[int, str]:
        n = Decoder.length_type_id[length_type]
        return self._get_data(s, n)

    def _get_type_id(self, s: str) -> Tuple[int, str]:
        return self._get_data(s, 3)

    def _get_data(self, s: str, i: int) -> Tuple[int, str]:
        data, rest = self._split(s, i)
        return self.bin_to_dec(data), rest

    def _split(self, s: str, i: int) -> Tuple[str, str]:
        return s[:i], s[i:]


def solve(filename: str = "input") -> List[Tuple[int, int]]:
    data = []
    with open(f"day16/{filename}", 'r') as f:
        while (line := f.readline().strip()):
            data.append(line)
    decoder = Decoder()
    answer = []
    for line in data:
        packet, _ = decoder.decode(line)
        answer.append((packet.version_sum(), packet.value()))
    return answer


print(solve())
