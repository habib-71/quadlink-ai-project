"""
QuadLink Board Renderer
-----------------------
Handles drawing the Connect Four board.
"""

import pygame

from config import (
    BOARD_BLUE,
    RED,
    YELLOW,
    WHITE,
)


class BoardRenderer:
    """
    Draws the Connect Four board.
    """

    def __init__(self):

        self.cell_size = 80

        self.board_x = 320
        self.board_y = 120

        self.preview_radius = 30

    def draw(self, screen, board):
        """
        Draw board and pieces.
        """

        # Draw board background

        pygame.draw.rect(
            screen,
            BOARD_BLUE,
            (
                self.board_x,
                self.board_y,
                self.cell_size * board.COLS,
                self.cell_size * board.ROWS
            ),
            border_radius=20
        )

        # Draw cells

        for row in range(board.ROWS):

            for col in range(board.COLS):

                center_x = (
                    self.board_x
                    + col * self.cell_size
                    + self.cell_size // 2
                )

                center_y = (
                    self.board_y
                    + row * self.cell_size
                    + self.cell_size // 2
                )

                value = board.grid[row][col]

                color = WHITE

                if value == board.PLAYER:
                    color = RED

                elif value == board.AI:
                    color = YELLOW

                pygame.draw.circle(
                    screen,
                    color,
                    (
                        center_x,
                        center_y
                    ),
                    30
                )

    def draw_hover_piece(self, screen, mouse_x, board):
        """
        Draw preview piece above the selected column.
        """

        # Ignore mouse outside board

        if (
            mouse_x < self.board_x
            or
            mouse_x > self.board_x + board.COLS * self.cell_size
        ):
            return

        col = (
            mouse_x - self.board_x
        ) // self.cell_size

        # Ignore full columns

        if not board.is_valid_move(col):
            return

        center_x = (
            self.board_x
            + col * self.cell_size
            + self.cell_size // 2
        )

        center_y = self.board_y - 45

        pygame.draw.circle(
            screen,
            RED,
            (
                center_x,
                center_y
            ),
            self.preview_radius
        )