from ai import AIPlayer
from board import Board
from hard_ai import HardAI


def test_easy_ai_takes_immediate_win():
    board = Board()
    for col in (0, 1, 2):
        board.drop_piece(col, board.AI)
    assert AIPlayer().get_move(board) == 3


def test_hard_ai_uses_minimax_to_block_forced_win():
    board = Board()
    for col in (0, 1, 2):
        board.drop_piece(col, board.PLAYER)
    assert HardAI().get_move(board) == 3
