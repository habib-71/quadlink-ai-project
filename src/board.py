"""Connect Four board state and rule checks."""


class Board:
    ROWS = 6
    COLS = 7
    EMPTY = 0
    PLAYER = 1
    AI = 2
    WIN_DIRECTIONS = ((0, 1), (1, 0), (1, 1), (-1, 1))

    def __init__(self):
        self.grid = [[self.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def is_valid_move(self, col):
        return isinstance(col, int) and 0 <= col < self.COLS and self.grid[0][col] == self.EMPTY

    def get_drop_row(self, col):
        if not self.is_valid_move(col):
            return -1
        for row in range(self.ROWS - 1, -1, -1):
            if self.grid[row][col] == self.EMPTY:
                return row
        return -1

    def drop_piece(self, col, player):
        row = self.get_drop_row(col)
        if row != -1:
            self.grid[row][col] = player
        return row

    def undo_piece(self, row, col):
        """Remove a known simulated move; used by the hard AI search."""
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            self.grid[row][col] = self.EMPTY

    def check_winner(self, player):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col] != player:
                    continue
                for row_step, col_step in self.WIN_DIRECTIONS:
                    end_row = row + row_step * 3
                    end_col = col + col_step * 3
                    if not (0 <= end_row < self.ROWS and 0 <= end_col < self.COLS):
                        continue
                    if all(self.grid[row + row_step * offset][col + col_step * offset] == player for offset in range(1, 4)):
                        return True
        return False

    def get_valid_moves(self):
        return [col for col in range(self.COLS) if self.is_valid_move(col)]

    def is_full(self):
        return not any(self.grid[0][col] == self.EMPTY for col in range(self.COLS))

    def reset(self):
        self.grid = [[self.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]
