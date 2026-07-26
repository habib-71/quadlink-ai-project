"""
QuadLink Main Menu
------------------
Handles the main menu screen.
"""

import pygame

from config import (
    SCREEN_WIDTH,
    BOARD_BLUE,
    TEXT_COLOR,
)

from ui import Button


class Menu:

    def __init__(
        self,
        title_font,
        button_font
    ):

        self.title_font = title_font
        self.button_font = button_font


        self.buttons = [

            Button(
                425,
                260,
                350,
                60,
                "Human vs AI",
                button_font
            ),

            Button(
                425,
                340,
                350,
                60,
                "Human vs Human",
                button_font
            ),

            Button(
                425,
                420,
                350,
                60,
                "Settings",
                button_font
            ),

            Button(
                425,
                500,
                350,
                60,
                "Statistics",
                button_font
            ),

            Button(
                425,
                580,
                350,
                60,
                "Exit",
                button_font
            ),
        ]


    def update(self):

        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:

            button.update(mouse_pos)



    def handle_click(self):

        mouse_pos = pygame.mouse.get_pos()

        mouse_pressed = pygame.mouse.get_pressed()[0]


        if mouse_pressed:

            for button in self.buttons:

                if button.clicked(
                    mouse_pos,
                    mouse_pressed
                ):

                    return button.text


        return None



    def draw(self, screen):

        title = self.title_font.render(
            "QUADLINK",
            True,
            BOARD_BLUE
        )


        screen.blit(
            title,
            (
                SCREEN_WIDTH // 2
                - title.get_width() // 2,
                60
            )
        )


        subtitle = self.button_font.render(
            "Strategic Connect Four",
            True,
            TEXT_COLOR
        )


        screen.blit(
            subtitle,
            (
                SCREEN_WIDTH // 2
                - subtitle.get_width() // 2,
                140
            )
        )


        for button in self.buttons:

            button.draw(screen)