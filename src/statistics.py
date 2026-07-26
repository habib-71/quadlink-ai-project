"""Runtime statistics screen for QuadLink."""

import pygame

from config import POP_BOLD, POP_REGULAR, SCREEN_WIDTH, TEXT_COLOR, TEXT_MUTED
from ui import Button, draw_card


class GameStats:
    """Keeps completed-game totals for the current application session."""

    def __init__(self):
        self.games_played = 0
        self.moves_played = 0
        self.player_one_wins = 0
        self.player_two_wins = 0
        self.ai_wins = 0
        self.draws = 0

    def record_move(self):
        self.moves_played += 1

    def record_result(self, mode, winner=None):
        self.games_played += 1
        if winner is None:
            self.draws += 1
        elif mode == "PVP":
            if winner == 1:
                self.player_one_wins += 1
            else:
                self.player_two_wins += 1
        elif winner == 1:
            self.player_one_wins += 1
        else:
            self.ai_wins += 1

    def reset(self):
        self.__init__()

    def to_dict(self):
        return {
            "games_played": self.games_played,
            "moves_played": self.moves_played,
            "player_one_wins": self.player_one_wins,
            "player_two_wins": self.player_two_wins,
            "ai_wins": self.ai_wins,
            "draws": self.draws,
        }

    def load_dict(self, values):
        for key in self.to_dict():
            value = values.get(key, 0)
            setattr(self, key, value if isinstance(value, int) and value >= 0 else 0)


class Statistics:
    """Displays session statistics with reset and back actions."""

    def __init__(self, stats):
        self.stats = stats
        self.title_font = pygame.font.Font(POP_BOLD, 44)
        self.value_font = pygame.font.Font(POP_BOLD, 30)
        self.body_font = pygame.font.Font(POP_REGULAR, 17)
        self.button_font = pygame.font.Font(POP_REGULAR, 17)
        self.reset_button = Button(410, 584, 180, 48, "Reset stats", self.button_font)
        self.back_button = Button(610, 584, 180, 48, "←  Back", self.button_font, accent=True)

    def update(self, mouse, delta_time=1 / 60):
        self.reset_button.update(mouse, delta_time)
        self.back_button.update(mouse, delta_time)

    def handle_click(self, mouse):
        if self.reset_button.clicked(mouse):
            self.stats.reset()
            return "reset"
        if self.back_button.clicked(mouse):
            return "back"
        return None

    def draw_metric(self, screen, rect, label, value):
        draw_card(screen, rect, radius=18)
        value_surface = self.value_font.render(str(value), True, TEXT_COLOR)
        label_surface = self.body_font.render(label, True, TEXT_MUTED)
        screen.blit(value_surface, value_surface.get_rect(center=(rect.centerx, rect.y + 42)))
        screen.blit(label_surface, label_surface.get_rect(center=(rect.centerx, rect.y + 82)))

    def draw(self, screen):
        title = self.title_font.render("Session statistics", True, TEXT_COLOR)
        subtitle = self.body_font.render("Your results for this QuadLink session.", True, TEXT_MUTED)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 142)))
        screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 188)))

        metrics = [
            ("Games played", self.stats.games_played),
            ("Moves played", self.stats.moves_played),
            ("Player 1 wins", self.stats.player_one_wins),
            ("Player 2 wins", self.stats.player_two_wins),
            ("AI wins", self.stats.ai_wins),
            ("Draws", self.stats.draws),
        ]
        for index, (label, value) in enumerate(metrics):
            row, col = divmod(index, 3)
            self.draw_metric(screen, pygame.Rect(300 + col * 204, 246 + row * 132, 180, 108), label, value)
        self.reset_button.draw(screen)
        self.back_button.draw(screen)
