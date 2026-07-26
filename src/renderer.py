"""Polished Connect Four board rendering and disc presentation."""

import pygame

from config import BOARD_BLUE, BOARD_DARK, RED, RED_LIGHT, SCREEN_WIDTH, WHITE, YELLOW, YELLOW_LIGHT
from ui import draw_shadow, lerp_color


class BoardRenderer:
    def __init__(self):
        self.cell_size = 80
        self.board_x = (SCREEN_WIDTH - self.cell_size * 7) // 2
        self.board_y = 166
        self.preview_radius = 29
        self.piece_radius = 29
        self.hover_col = None
        self.hover_amount = 0.0

    def update_hover(self, mouse_x, board, delta_time):
        col = None
        if self.board_x <= mouse_x < self.board_x + board.COLS * self.cell_size:
            candidate = (mouse_x - self.board_x) // self.cell_size
            if board.is_valid_move(candidate):
                col = candidate
        self.hover_col = col
        target = 1.0 if col is not None else 0.0
        self.hover_amount += (target - self.hover_amount) * min(1.0, delta_time * 14)

    def draw(self, screen, board):
        board_rect = pygame.Rect(self.board_x, self.board_y, self.cell_size * board.COLS, self.cell_size * board.ROWS)
        draw_shadow(screen, board_rect, radius=26, offset=10, alpha=130)
        pygame.draw.rect(screen, BOARD_DARK, board_rect, border_radius=26)
        inner = board_rect.inflate(-8, -8)
        pygame.draw.rect(screen, BOARD_BLUE, inner, border_radius=22)

        for row in range(board.ROWS):
            for col in range(board.COLS):
                center_x, center_y = self.get_cell_center(row, col)
                value = board.grid[row][col]
                pygame.draw.circle(screen, (25, 36, 76), (center_x, center_y + 3), self.piece_radius + 3)
                pygame.draw.circle(screen, (232, 238, 255), (center_x, center_y), self.piece_radius)
                if value != board.EMPTY:
                    color = RED if value == board.PLAYER else YELLOW
                    highlight = RED_LIGHT if value == board.PLAYER else YELLOW_LIGHT
                    self.draw_disc(screen, center_x, center_y, color, highlight)

    def draw_disc(self, screen, x, y, color, highlight):
        pygame.draw.circle(screen, (13, 19, 41), (x, y + 3), self.piece_radius)
        pygame.draw.circle(screen, color, (x, y), self.piece_radius)
        pygame.draw.circle(screen, highlight, (x - 8, y - 9), max(4, self.piece_radius // 5))
        pygame.draw.circle(screen, lerp_color(color, (255, 255, 255), 0.2), (x, y), self.piece_radius, width=2)

    def draw_hover_piece(self, screen, mouse_x, board, player=1):
        if self.hover_col is None or self.hover_amount <= 0.02:
            return
        center_x = self.board_x + self.hover_col * self.cell_size + self.cell_size // 2
        center_y = self.board_y - 42 - int(self.hover_amount * 4)
        radius = int(self.preview_radius * self.hover_amount)
        preview = pygame.Surface((80, 80), pygame.SRCALPHA)
        color = RED if player == 1 else YELLOW
        highlight = RED_LIGHT if player == 1 else YELLOW_LIGHT
        pygame.draw.circle(preview, (*color, int(190 * self.hover_amount)), (40, 40), radius)
        pygame.draw.circle(preview, (*highlight, int(180 * self.hover_amount)), (32, 31), max(3, radius // 5))
        screen.blit(preview, (center_x - 40, center_y - 40))

    def draw_falling_piece(self, screen, col, current_y, player):
        center_x = self.board_x + col * self.cell_size + self.cell_size // 2
        color = RED if player == 1 else YELLOW
        highlight = RED_LIGHT if player == 1 else YELLOW_LIGHT
        self.draw_disc(screen, center_x, int(current_y), color, highlight)

    def get_cell_center(self, row, col):
        return (
            self.board_x + col * self.cell_size + self.cell_size // 2,
            self.board_y + row * self.cell_size + self.cell_size // 2,
        )
