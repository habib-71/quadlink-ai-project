"""
QuadLink AI System
------------------
Handles computer moves.
"""

import random


class AIPlayer:


    def __init__(self):

        self.name = "QuadLink AI"



    def get_move(self, board):
        """
        Selects a valid move.

        Current version:
        Random AI
        """


        valid_moves = (
            board.get_valid_moves()
        )


        if not valid_moves:

            return None


        return random.choice(
            valid_moves
        )