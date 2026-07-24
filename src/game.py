"""
QuadLink Game Controller
------------------------
Controls the main game loop.
"""

import sys
import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GAME_TITLE,
    BACKGROUND,
    TEXT_COLOR,
    BOARD_BLUE,
    POP_BOLD,
    POP_REGULAR,
)


class Game:
    """Main Game Controller."""

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()

        # Load Fonts
        self.title_font = pygame.font.Font(
            POP_BOLD,
            56
        )

        self.subtitle_font = pygame.font.Font(
            POP_REGULAR,
            24
        )

        self.running = True

    def handle_events(self):
        """Handle user input."""

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Update game state."""
        pass

    def draw(self):
        """Draw everything."""

        self.screen.fill(BACKGROUND)

        # Title
        title = self.title_font.render(
            "QUADLINK",
            True,
            BOARD_BLUE
        )

        self.screen.blit(
            title,
            (
                SCREEN_WIDTH // 2 - title.get_width() // 2,
                60,
            ),
        )

        # Subtitle
        subtitle = self.subtitle_font.render(
            "Strategic Connect Four",
            True,
            TEXT_COLOR
        )

        self.screen.blit(
            subtitle,
            (
                SCREEN_WIDTH // 2 - subtitle.get_width() // 2,
                130,
            ),
        )

        pygame.display.flip()

    def run(self):
        """Main Game Loop."""

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
        