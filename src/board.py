"""
QuadLink Board System
---------------------
Handles Connect Four board logic.
"""


class Board:

    ROWS = 6
    COLS = 7

    EMPTY = 0
    PLAYER = 1
    AI = 2


    def __init__(self):

        self.grid = [
            [self.EMPTY for _ in range(self.COLS)]
            for _ in range(self.ROWS)
        ]



    def is_valid_move(self, col):

        if col < 0 or col >= self.COLS:
            return False

        return self.grid[0][col] == self.EMPTY



    def drop_piece(self, col, player):

        if not self.is_valid_move(col):
            return -1


        for row in range(
            self.ROWS - 1,
            -1,
            -1
        ):

            if self.grid[row][col] == self.EMPTY:

                self.grid[row][col] = player

                return row


        return -1




    def check_winner(self, player):


        # Horizontal ----

        for row in range(self.ROWS):

            for col in range(self.COLS - 3):

                if (
                    self.grid[row][col] == player and
                    self.grid[row][col+1] == player and
                    self.grid[row][col+2] == player and
                    self.grid[row][col+3] == player
                ):
                    return True



        # Vertical |

        for row in range(self.ROWS - 3):

            for col in range(self.COLS):

                if (
                    self.grid[row][col] == player and
                    self.grid[row+1][col] == player and
                    self.grid[row+2][col] == player and
                    self.grid[row+3][col] == player
                ):
                    return True




        # Diagonal \

        for row in range(self.ROWS - 3):

            for col in range(self.COLS - 3):

                if (
                    self.grid[row][col] == player and
                    self.grid[row+1][col+1] == player and
                    self.grid[row+2][col+2] == player and
                    self.grid[row+3][col+3] == player
                ):
                    return True




        # Diagonal /

        for row in range(3, self.ROWS):

            for col in range(self.COLS - 3):

                if (
                    self.grid[row][col] == player and
                    self.grid[row-1][col+1] == player and
                    self.grid[row-2][col+2] == player and
                    self.grid[row-3][col+3] == player
                ):
                    return True



        return False




    def get_valid_moves(self):

        moves = []

        for col in range(self.COLS):

            if self.is_valid_move(col):

                moves.append(col)


        return moves




    def is_full(self):

        return len(
            self.get_valid_moves()
        ) == 0




    def reset(self):

        self.grid = [
            [self.EMPTY for _ in range(self.COLS)]
            for _ in range(self.ROWS)
        ]