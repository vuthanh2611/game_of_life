from abc import abstractmethod, ABC
from time import sleep


class AbstractLifeGameBoard(ABC):
    def __init__(self, width: int = 3, height: int = 3):
        pass

    def __str__(self):
        """Return a string representation of a board.

        Use small o for alive cells and period for empty cells.
        E.g. for board 3x3 with simplest oscillator:
        .o.
        .o.
        .o.
        """
        pass

    @abstractmethod
    def place_cell(self, row: int, col: int):
        """Make a cell alive."""
        pass

    @abstractmethod
    def toggle_cell(self, row: int, col: int) -> None:
        """Invert state of the cell."""
        pass

    @abstractmethod
    def next(self) -> None:
        pass

    @abstractmethod
    def is_alive(self, row: int, col: int) -> bool:
        pass


class Board(AbstractLifeGameBoard):
    """Put your solution here"""

    def __init__(self, width: int = 3, height: int = 3):
        self.width = width
        self.height = height
        self.board = [[False for _ in range(width)] for _ in range(height)]

    def __str__(self):
        board_str = []
        for row in self.board:
            row_str = []
            for item in row:
                if not item:
                    row_str.append(". ")
                else:
                    row_str.append("o ")
            board_str.append("".join(row_str))
        return "\n".join(board_str)

    def next(self) -> None:
        new_board = [[False for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.width):
            for j in range(self.height):
                neighbors = self.count_neighbors(i, j)
                if self.board[i][j]:
                    if neighbors < 2 or neighbors > 3:
                        new_board[i][j] = False
                    else:
                        new_board[i][j] = True
                else:
                    if neighbors == 3:
                        new_board[i][j] = True
        self.board = new_board
        return self.board

    def count_neighbors(self, row: int, col: int) -> int:
        count = 0
        for i in range(max(0, row - 1), min(self.width, row + 2)):
            for j in range(max(0, col - 1), min(self.height, col + 2)):
                count += self.board[i][j]
        count -= self.board[row][col]
        return count

    def place_cell(self, row: int, col: int):
        self.board[row][col] = True

    def toggle_cell(self, row: int, col: int) -> None:
        if not self.board[row][col]:
            self.board[row][col] = True
        else:
            self.board[row][col] = False

    def is_alive(self, row: int, col: int) -> bool:
        if not self.board[row][col]:
            return False
        else:
            return True


c = CELL_SYMBOL = "o"

if __name__ == "__main__":
    board = Board(3, 3)
    for i in range(3):
        board.place_cell(1, i)

    for i in range(100):
        print(board)
        board.next()
        sleep(0.5)
