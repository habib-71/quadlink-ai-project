"""
QuadLink Hard AI
----------------
Minimax + Alpha-Beta Pruning
"""

import math
import random


class HardAI:

    AI = 2
    PLAYER = 1
    EMPTY = 0

    DEPTH = 5


    def get_move(self, board):

        valid_moves = board.get_valid_moves()

        if len(valid_moves) == 0:
            return None

        _, column = self.minimax(
            board,
            self.DEPTH,
            -math.inf,
            math.inf,
            True
        )

        if column is None:
            return random.choice(valid_moves)

        return column


    def minimax(
        self,
        board,
        depth,
        alpha,
        beta,
        maximizing
    ):

        valid_moves = board.get_valid_moves()

        terminal = (
            board.check_winner(self.AI)
            or board.check_winner(self.PLAYER)
            or board.is_full()
        )

        if depth == 0 or terminal:

            if board.check_winner(self.AI):
                return (1000000, None)

            if board.check_winner(self.PLAYER):
                return (-1000000, None)

            if board.is_full():
                return (0, None)

            return (
                self.score_position(board),
                None
            )


        if maximizing:

            value = -math.inf
            best_col = random.choice(valid_moves)

            for col in valid_moves:

                temp = self.copy_board(board)

                temp.drop_piece(col, self.AI)

                score, _ = self.minimax(
                    temp,
                    depth - 1,
                    alpha,
                    beta,
                    False
                )

                if score > value:

                    value = score
                    best_col = col

                alpha = max(alpha, value)

                if alpha >= beta:
                    break

            return value, best_col


        else:

            value = math.inf
            best_col = random.choice(valid_moves)

            for col in valid_moves:

                temp = self.copy_board(board)

                temp.drop_piece(
                    col,
                    self.PLAYER
                )

                score, _ = self.minimax(
                    temp,
                    depth - 1,
                    alpha,
                    beta,
                    True
                )

                if score < value:

                    value = score
                    best_col = col

                beta = min(beta, value)

                if alpha >= beta:
                    break

            return value, best_col


    def score_position(
        self,
        board
    ):

        score = 0

        center = []

        for r in range(board.ROWS):

            center.append(
                board.grid[r][board.COLS // 2]
            )

        score += (
            center.count(self.AI) * 6
        )

        # Horizontal

        for r in range(board.ROWS):

            row = board.grid[r]

            for c in range(board.COLS - 3):

                window = row[c:c+4]

                score += self.evaluate(window)

        # Vertical

        for c in range(board.COLS):

            col = []

            for r in range(board.ROWS):
                col.append(board.grid[r][c])

            for r in range(board.ROWS - 3):

                window = col[r:r+4]

                score += self.evaluate(window)

        # Positive diagonal

        for r in range(board.ROWS - 3):

            for c in range(board.COLS - 3):

                window = [
                    board.grid[r+i][c+i]
                    for i in range(4)
                ]

                score += self.evaluate(window)

        # Negative diagonal

        for r in range(3, board.ROWS):

            for c in range(board.COLS - 3):

                window = [
                    board.grid[r-i][c+i]
                    for i in range(4)
                ]

                score += self.evaluate(window)

        return score


    def evaluate(
        self,
        window
    ):

        score = 0

        if window.count(self.AI) == 4:
            score += 100

        elif (
            window.count(self.AI) == 3
            and window.count(self.EMPTY) == 1
        ):
            score += 15

        elif (
            window.count(self.AI) == 2
            and window.count(self.EMPTY) == 2
        ):
            score += 5

        if (
            window.count(self.PLAYER) == 3
            and window.count(self.EMPTY) == 1
        ):
            score -= 20

        if (
            window.count(self.PLAYER) == 4
        ):
            score -= 100

        return score


    def copy_board(
        self,
        board
    ):

        from board import Board

        new_board = Board()

        new_board.grid = [
            row[:]
            for row in board.grid
        ]

        return new_board