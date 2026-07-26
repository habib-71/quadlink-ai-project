"""Runtime visual and audio preferences for QuadLink."""

import pygame

from config import POP_BOLD, POP_REGULAR, SCREEN_WIDTH, TEXT_COLOR, TEXT_MUTED
from ui import Button, draw_card


class Settings:
    """Presents session-only preferences without touching game mechanics."""

    def __init__(self, sound_enabled=True, music_enabled=True, animation_enabled=True):
        self.title_font = pygame.font.Font(POP_BOLD, 44)
        self.body_font = pygame.font.Font(POP_REGULAR, 18)
        self.button_font = pygame.font.Font(POP_REGULAR, 17)
        self.values = {
            "sound": sound_enabled,
            "music": music_enabled,
            "animation": animation_enabled,
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
        self.back_button = Button(492, 592, 216, 48, "←  Back to menu", self.button_font)

    def update(self, delta_time=1 / 60):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        for index, (key, _, _) in enumerate(self.rows):
            button = self.toggle_buttons[key]
            button.rect.y = 290 + index * 86
            button.text = "ON" if self.values[key] else "OFF"
            button.update(mouse, pressed, delta_time)
        self.back_button.update(mouse, pressed, delta_time)

    def handle_click(self):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        for key, _, _ in self.rows:
            if self.toggle_buttons[key].clicked(mouse, pressed):
                self.values[key] = not self.values[key]
                return key
        if self.back_button.clicked(mouse, pressed):
            return "back"
        return None

    def draw(self, screen):
        title = self.title_font.render("Settings", True, TEXT_COLOR)
        subtitle = self.body_font.render("Preferences are saved while QuadLink is running.", True, TEXT_MUTED)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 150)))
        screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 198)))

        panel = pygame.Rect(326, 246, 548, 310)
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
        self.back_button.draw(screen)
