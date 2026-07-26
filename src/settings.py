"""Runtime visual and audio preferences for QuadLink."""

import pygame

from config import POP_BOLD, POP_REGULAR, SCREEN_WIDTH, TEXT_COLOR, TEXT_MUTED, PRIMARY, SURFACE_BORDER
from ui import Button, draw_card


class Settings:
    """Presents session-only preferences without touching game mechanics."""

    def __init__(self, sound_enabled=True, music_enabled=True, animation_enabled=True, volume=0.35):
        self.title_font = pygame.font.Font(POP_BOLD, 44)
        self.body_font = pygame.font.Font(POP_REGULAR, 18)
        self.button_font = pygame.font.Font(POP_REGULAR, 17)
        self.values = {
            "sound": sound_enabled,
            "music": music_enabled,
            "animation": animation_enabled,
            "volume": max(0.0, min(1.0, float(volume))),
        }
        self.rows = [
            ("sound", "Sound effects", "Click, disc, and result effects."),
            ("music", "Background music", "Controls optional background music."),
            ("animation", "Drop animations", "Show discs falling into position."),
        ]
        self.toggle_buttons = {
            key: Button(704, 0, 126, 44, "", self.button_font, accent=True)
            for key, _, _ in self.rows
        }
        self.volume_rect = pygame.Rect(704, 546, 126, 8)
        self.back_button = Button(492, 620, 216, 48, "←  Back to menu", self.button_font)

    def update(self, mouse, delta_time=1 / 60):
        for index, (key, _, _) in enumerate(self.rows):
            button = self.toggle_buttons[key]
            button.rect.y = 290 + index * 86
            button.text = "ON" if self.values[key] else "OFF"
            button.update(mouse, delta_time)
        self.back_button.update(mouse, delta_time)

    def handle_click(self, mouse):
        for key, _, _ in self.rows:
            if self.toggle_buttons[key].clicked(mouse):
                self.values[key] = not self.values[key]
                return key
        if self.volume_rect.inflate(10, 24).collidepoint(mouse):
            self.values["volume"] = max(0.0, min(1.0, (mouse[0] - self.volume_rect.x) / self.volume_rect.width))
            return "volume"
        if self.back_button.clicked(mouse):
            return "back"
        return None

    def draw(self, screen):
        title = self.title_font.render("Settings", True, TEXT_COLOR)
        subtitle = self.body_font.render("Preferences are saved between sessions.", True, TEXT_MUTED)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 150)))
        screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 198)))

        panel = pygame.Rect(326, 246, 548, 364)
        draw_card(screen, panel, radius=24)
        for index, (key, label, description) in enumerate(self.rows):
            y = 274 + index * 86
            if index:
                pygame.draw.line(screen, (67, 89, 137), (356, y - 15), (844, y - 15), 1)
            label_surface = self.body_font.render(label, True, TEXT_COLOR)
            description_surface = self.button_font.render(description, True, TEXT_MUTED)
            screen.blit(label_surface, (360, y + 4))
            screen.blit(description_surface, (360, y + 30))
            self.toggle_buttons[key].draw(screen)
        volume_label = self.body_font.render("Music volume", True, TEXT_COLOR)
        volume_value = self.button_font.render(f"{round(self.values['volume'] * 100)}%", True, TEXT_MUTED)
        screen.blit(volume_label, (360, 532))
        screen.blit(volume_value, (610, 532))
        pygame.draw.rect(screen, SURFACE_BORDER, self.volume_rect, border_radius=4)
        filled = self.volume_rect.copy()
        filled.width = int(self.volume_rect.width * self.values["volume"])
        pygame.draw.rect(screen, PRIMARY, filled, border_radius=4)
        knob_x = self.volume_rect.x + int(self.volume_rect.width * self.values["volume"])
        pygame.draw.circle(screen, TEXT_COLOR, (knob_x, self.volume_rect.centery), 8)
        self.back_button.draw(screen)
