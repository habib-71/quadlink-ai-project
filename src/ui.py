"""
QuadLink UI Components
---------------------
Contains reusable UI elements like buttons.
"""

import pygame

from config import (
    BOARD_BLUE,
    WHITE,
)


class Button:
    """
    Reusable button component.
    """

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font
    ):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.text = text
        self.font = font

        self.normal_color = BOARD_BLUE

        self.hover_color = (
            30,
            80,
            200
        )

        self.text_color = WHITE

        self.is_hovered = False



    def update(self, mouse_pos):

        self.is_hovered = self.rect.collidepoint(
            mouse_pos
        )



    def draw(self, screen):

        color = (
            self.hover_color
            if self.is_hovered
            else self.normal_color
        )


        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=15
        )


        text_surface = self.font.render(
            self.text,
            True,
            self.text_color
        )


        screen.blit(
            text_surface,
            (
                self.rect.centerx
                - text_surface.get_width() // 2,

                self.rect.centery
                - text_surface.get_height() // 2
            )
        )



    def clicked(self, mouse_pos, mouse_pressed):
        """
        Returns True when button clicked.
        """

        return (
            self.rect.collidepoint(mouse_pos)
            and mouse_pressed
        )