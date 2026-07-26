"""Difficulty selection screen with animated choice cards."""

import pygame

from config import POP_BOLD, POP_REGULAR, SCREEN_WIDTH, TEXT_COLOR, TEXT_MUTED
from ui import DifficultyCard


class Difficulty:
    def __init__(self):
        self.title_font = pygame.font.Font(POP_BOLD, 44)
        self.card_font = pygame.font.Font(POP_BOLD, 28)
        self.body_font = pygame.font.Font(POP_REGULAR, 18)
        self.cards = {
            "Easy": DifficultyCard("Easy", "A relaxed opponent that picks valid moves.", (320, 270, 560, 130), self.card_font, self.body_font),
            "Hard": DifficultyCard("Hard", "A strategic opponent using minimax search.", (320, 424, 560, 130), self.card_font, self.body_font),
        }
        self.selected = "Easy"

    def update(self, mouse, delta_time=1 / 60):
        for card in self.cards.values():
            card.update(mouse, delta_time)

    def draw(self, screen):
        title = self.title_font.render("Choose your challenge", True, TEXT_COLOR)
        subtitle = self.body_font.render("You can start a fresh game at any difficulty.", True, TEXT_MUTED)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 154)))
        screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 202)))
        for name, card in self.cards.items():
            card.draw(screen, selected=name == self.selected)

    def handle_click(self, mouse):
        for name, card in self.cards.items():
            if card.clicked(mouse):
                self.selected = name
                return name
        return None
