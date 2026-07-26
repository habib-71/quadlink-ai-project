"""Responsive easy-mode Connect Four opponent."""

import random


class AIPlayer:
    """Chooses immediate wins and blocks before making a lightweight random move."""

    def __init__(self):
        self.name = "QuadLink AI"

    def get_move(self, board):
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None

        for player in (board.AI, board.PLAYER):
            for col in valid_moves:
                row = board.drop_piece(col, player)
                won = board.check_winner(player)
                board.undo_piece(row, col)
                if won:
                    return col

        center_first = sorted(valid_moves, key=lambda col: abs(col - board.COLS // 2))
        best_distance = abs(center_first[0] - board.COLS // 2)
        preferred = [col for col in center_first if abs(col - board.COLS // 2) == best_distance]
        return random.choice(preferred)
