"""QuadLink's animated main menu."""

import pygame

from config import SCREEN_WIDTH, TEXT_COLOR, TEXT_MUTED
from ui import Button, draw_card


class Menu:
    def __init__(self, title_font, button_font):
        self.title_font = title_font
        self.button_font = button_font
        self.buttons = [
            Button(425, 310, 350, 58, "Play vs AI", button_font, accent=True),
            Button(425, 386, 350, 58, "Play vs Player", button_font),
            Button(425, 462, 350, 58, "Settings", button_font),
            Button(425, 538, 350, 58, "Statistics", button_font),
            Button(425, 614, 350, 50, "Exit", button_font),
        ]

    def update(self, delta_time=1 / 60):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        for button in self.buttons:
            button.update(mouse_pos, mouse_pressed, delta_time)

    def handle_click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        for button in self.buttons:
            if button.clicked(mouse_pos, mouse_pressed):
                if button.text == "Play vs AI":
                    return "Human vs AI"
                if button.text == "Play vs Player":
                    return "Human vs Human"
                return button.text
        return None

    def draw(self, screen):
        title = self.title_font.render("QUADLINK", True, TEXT_COLOR)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 116)))
        subtitle = self.button_font.render("A considered game of four in a row", True, TEXT_MUTED)
        screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 172)))

        panel = pygame.Rect(380, 248, 440, 444)
        draw_card(screen, panel, radius=26)
        label = self.button_font.render("NEW GAME", True, TEXT_MUTED)
        screen.blit(label, label.get_rect(center=(SCREEN_WIDTH // 2, 278)))
        for button in self.buttons:
            button.draw(screen)
