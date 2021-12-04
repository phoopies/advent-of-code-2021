from typing import List, Tuple, Union
from colorama import Style

def colorize(s:str, color) -> str:
    return color + s + Style.RESET_ALL

class Entry:
    def __init__(self, value: int, marked: bool = False) -> None:
        self.value = value
        self.marked = marked
    
    def __str__(self) -> str:
        return colorize(str(self.value), Style.BRIGHT) if self.marked else colorize(str(self.value), Style.DIM)
    
    def mark(self) -> None:
        self.marked = True


class Bingo:
    def __init__(self, board: Union[List[List[int]], List[List[Entry]], int] = 0) -> None:
        if isinstance(board, int): self.board = [[Entry(0) for _ in range(board)] for _ in range(board)]
        else: self.board = board if all(isinstance(entry, Entry) for entry in board) else [[Entry(i) for i in row] for row in board]
    
    def __setitem__(self, key: Tuple[int], value: int) -> None:
        self.board[key[0]][key[1]] = value
    
    def __getitem__(self, key: Tuple[int]) -> int:
        return self.board[key[0]][key[1]] 
    
    def __str__(self) -> str:
        return "\n".join([" ".join([str(entry) for entry in row]) for row in self.board])
    
    def __len__(self) -> int:
        return len(self.board[0])
    
    def set_row(self, i: int, row: Union[List[Entry], List[int]]) -> None:
        self.board[i] = row
    
    def add_row(self, row: Union[List[Entry], List[int]]) -> None:
        entries = row if all(isinstance(entry, Entry) for entry in row) else [Entry(i) for i in row]
        self.board.append(entries)
    
    def mark(self, value: int) -> None:
        key = self._find(value)
        if (key[0] >= 0):
            self._mark(key)

    def _mark(self, key: Tuple[int]) -> None:
        self[key].mark()
    
    def won(self) -> bool:
        return self._check_rows() or self._check_columns()
    
    def sum_unmarked(self) -> int:
        sum = 0
        for row in self.board:
            for entry in row:
                if not entry.marked: sum += entry.value
        return sum
    
    # Linear search
    def _find(self, value: int) -> Tuple[int]:
        for x, row in enumerate(self.board):
            for y, entry in enumerate(row):
                if entry.value == value: return (x,y)
        return (-1, -1)

    def _check_rows(self) -> bool:
        return any(all(entry.marked for entry in row) for row in self.board)
    
    def _check_columns(self) -> bool:
        for i in range(len(self)):
            if all(entry.marked for entry in self._get_column(i)): return True
        return False
    
    def _get_column(self, i: int) -> List[Entry]:
        column = []
        for row in self.board:
            column.append(row[i])
        return column

def parse_numbers(s:str, sep:str) -> List[int]:
    values = s.strip().split(sep)
    numbers = [int(value) for value in values if value.isdigit()]
    return numbers

def get_input(filename: str = "input") -> Tuple[List[int], List[Bingo]]:
    numbers: List[int] = []
    boards: List[Bingo] = []
    with open(f"day4/{filename}", 'r') as f:
        line = f.readline().strip()
        numbers = parse_numbers(line, ',')
        while line := f.readline():
            if line == "\n":
                line = f.readline()
                boards.append(Bingo())
            row = parse_numbers(line, ' ')
            boards[-1].add_row(row)
    return numbers, boards

def winners(number: int, boards: List[Bingo]) -> List[Bingo]:
    round_winners: List[Bingo] = []
    for board in boards:
        board.mark(number)
        if board.won(): round_winners.append(board)
    return round_winners

def winner(numbers: List[int], boards: List[Bingo], first:bool = True) -> Tuple[int, Bingo]:
    for number in numbers:
        round_winners = winners(number, boards)
        if len(round_winners) > 0:
            if first: return number, round_winners[0] # return the board that won first
            for round_winner in round_winners: boards.remove(round_winner) # remove all winners
            if len(boards) == 0: return number, round_winners[-1] # If all removed return the last winner of current round
    return -1, Bingo()

def first_winner(numbers: List[int], boards: List[Bingo]) -> Tuple[int, Bingo]:
    return winner(numbers, boards, True)

def last_winner(numbers: List[int], boards: List[Bingo]) -> Tuple[int, Bingo]:
    return winner(numbers, boards, False)

def solve(part_two = False, filename: str = "input"):
    numbers, boards = get_input(filename)
    last_number, board = last_winner(numbers, boards) if part_two else first_winner(numbers, boards)
    return last_number * board.sum_unmarked(), board


if __name__ == "__main__":
    # test_board = Bingo([[1,2,3], [4,5,6], [7,8,9]])
    # for i in [1,4,5,8]:
    #     test_board.mark(i)
    # print(str(test_board))
    # print(test_board.won())
    # print("*"*50)
    # test_board.mark(7)
    # print(test_board)
    # print(test_board.won())
    result, board = solve(True)
    print(board)
    print("*"*50)
    print(f"result is {result}")
