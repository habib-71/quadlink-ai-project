from board import Board


def test_drop_and_valid_moves():
    board = Board()
    assert board.drop_piece(3, board.PLAYER) == 5
    assert board.grid[5][3] == board.PLAYER
    assert 3 in board.get_valid_moves()


def test_detects_horizontal_winning_cells():
    board = Board()
    for col in range(4):
        board.drop_piece(col, board.PLAYER)
    assert board.check_winner(board.PLAYER)
    assert board.get_winning_cells(board.PLAYER) == ((5, 0), (5, 1), (5, 2), (5, 3))


def test_rejects_full_column_and_copy_is_independent():
    board = Board()
    for _ in range(board.ROWS):
        board.drop_piece(0, board.PLAYER)
    assert not board.is_valid_move(0)
    clone = board.copy()
    clone.drop_piece(1, board.AI)
    assert board.grid[5][1] == board.EMPTY
