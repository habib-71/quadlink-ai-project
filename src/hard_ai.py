"""Hard Connect Four AI using ordered alpha-beta minimax."""

import math


class HardAI:
    AI = 2
    PLAYER = 1
    EMPTY = 0
    DEPTH = 5
    MOVE_ORDER = (3, 2, 4, 1, 5, 0, 6)
    WIN_SCORE = 1_000_000

    def get_move(self, board):
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None
        _, column = self.minimax(board, self.DEPTH, -math.inf, math.inf, True)
        return column if column is not None else valid_moves[0]

    def ordered_moves(self, board):
        valid = set(board.get_valid_moves())
        return [col for col in self.MOVE_ORDER if col in valid]

    def minimax(self, board, depth, alpha, beta, maximizing):
        ai_won = board.check_winner(self.AI)
        player_won = board.check_winner(self.PLAYER)
        if ai_won:
            return self.WIN_SCORE + depth, None
        if player_won:
            return -self.WIN_SCORE - depth, None
        if board.is_full():
            return 0, None
        if depth == 0:
            return self.score_position(board), None

        best_col = None
        if maximizing:
            value = -math.inf
            for col in self.ordered_moves(board):
                row = board.drop_piece(col, self.AI)
                score, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.undo_piece(row, col)
                if score > value:
                    value, best_col = score, col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_col

        value = math.inf
        for col in self.ordered_moves(board):
            row = board.drop_piece(col, self.PLAYER)
            score, _ = self.minimax(board, depth - 1, alpha, beta, True)
            board.undo_piece(row, col)
            if score < value:
                value, best_col = score, col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_col

    def score_position(self, board):
        score = sum(6 for row in range(board.ROWS) if board.grid[row][board.COLS // 2] == self.AI)
        for row in range(board.ROWS):
            for col in range(board.COLS - 3):
                score += self.evaluate([board.grid[row][col + offset] for offset in range(4)])
        for row in range(board.ROWS - 3):
            for col in range(board.COLS):
                score += self.evaluate([board.grid[row + offset][col] for offset in range(4)])
        for row in range(board.ROWS - 3):
            for col in range(board.COLS - 3):
                score += self.evaluate([board.grid[row + offset][col + offset] for offset in range(4)])
                score += self.evaluate([board.grid[row + 3 - offset][col + offset] for offset in range(4)])
        return score

    def evaluate(self, window):
        ai_count = window.count(self.AI)
        player_count = window.count(self.PLAYER)
        empty_count = window.count(self.EMPTY)
        if ai_count == 4:
            return 100
        if ai_count == 3 and empty_count == 1:
            return 15
        if ai_count == 2 and empty_count == 2:
            return 5
        if player_count == 3 and empty_count == 1:
            return -20
        if player_count == 4:
            return -100
        return 0
