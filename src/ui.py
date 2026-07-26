"""Reusable, lightweight visual components for QuadLink."""

import pygame

from config import BLACK, PRIMARY, PRIMARY_DARK, PRIMARY_HOVER, SURFACE, SURFACE_BORDER, SURFACE_LIGHT, TEXT_COLOR, TEXT_MUTED, WHITE


def lerp_color(start, end, amount):
    return tuple(int(a + (b - a) * amount) for a, b in zip(start, end))


def draw_shadow(surface, rect, radius=18, offset=6, alpha=100):
    shadow = pygame.Surface((rect.width + 24, rect.height + 24), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (*BLACK, alpha), (12, 12 + offset, rect.width, rect.height), border_radius=radius)
    surface.blit(shadow, (rect.x - 12, rect.y - 12))


def draw_card(surface, rect, fill=SURFACE, border=SURFACE_BORDER, radius=20, shadow=True):
    if shadow:
        draw_shadow(surface, rect, radius)
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, width=1, border_radius=radius)


class Button:
    """Rounded button with frame-rate independent hover and press feedback."""

    def __init__(self, x, y, width, height, text, font, accent=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.accent = accent
        self.hover_amount = 0.0
        self.press_amount = 0.0
        self.is_hovered = False
        self.just_pressed = False
        self.was_pressed = False

    def update(self, mouse_pos, delta_time=1 / 60):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        target_hover = 1.0 if self.is_hovered else 0.0
        target_press = 0.0
        self.hover_amount += (target_hover - self.hover_amount) * min(1.0, delta_time * 12)
        self.press_amount += (target_press - self.press_amount) * min(1.0, delta_time * 18)

    def draw(self, screen):
        base = PRIMARY if self.accent else SURFACE_LIGHT
        hover = PRIMARY_HOVER if self.accent else (48, 67, 112)
        color = lerp_color(base, hover, self.hover_amount)
        border = lerp_color(PRIMARY_DARK if self.accent else SURFACE_BORDER, PRIMARY_HOVER, self.hover_amount)
        lift = int(self.hover_amount * 4 - self.press_amount * 2)
        draw_rect = self.rect.move(0, -lift)
        draw_shadow(screen, draw_rect, radius=16, offset=5 - lift, alpha=90)
        if self.hover_amount > 0.08:
            glow = pygame.Surface((draw_rect.width + 16, draw_rect.height + 16), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*PRIMARY_HOVER, int(32 * self.hover_amount)), glow.get_rect(), border_radius=20)
            screen.blit(glow, (draw_rect.x - 8, draw_rect.y - 8))
        pygame.draw.rect(screen, color, draw_rect, border_radius=16)
        pygame.draw.rect(screen, border, draw_rect, width=1, border_radius=16)
        text = self.font.render(self.text, True, WHITE if self.accent else TEXT_COLOR)
        screen.blit(text, text.get_rect(center=draw_rect.center))

    def clicked(self, mouse_pos):
        """Handle a single MOUSEBUTTONDOWN event rather than held mouse state."""
        return self.rect.collidepoint(mouse_pos)


class DifficultyCard:
    """Selectable difficulty option with clear selected and hover states."""

    def __init__(self, name, subtitle, rect, font, small_font):
        self.name = name
        self.subtitle = subtitle
        self.rect = pygame.Rect(rect)
        self.font = font
        self.small_font = small_font
        self.hover_amount = 0.0

    def update(self, mouse_pos, delta_time):
        target = 1.0 if self.rect.collidepoint(mouse_pos) else 0.0
        self.hover_amount += (target - self.hover_amount) * min(1.0, delta_time * 12)

    def draw(self, screen, selected=False):
        lift = int(self.hover_amount * 5)
        rect = self.rect.move(0, -lift)
        fill = lerp_color(SURFACE, SURFACE_LIGHT, self.hover_amount)
        border = PRIMARY_HOVER if selected else lerp_color(SURFACE_BORDER, PRIMARY, self.hover_amount)
        draw_card(screen, rect, fill, border, 22)
        if selected:
            badge = self.small_font.render("SELECTED", True, WHITE)
            badge_rect = pygame.Rect(rect.right - badge.get_width() - 28, rect.y + 22, badge.get_width() + 16, badge.get_height() + 8)
            pygame.draw.rect(screen, PRIMARY, badge_rect, border_radius=badge_rect.height // 2)
            screen.blit(badge, badge.get_rect(center=badge_rect.center))
        title = self.font.render(self.name, True, TEXT_COLOR)
        subtitle = self.small_font.render(self.subtitle, True, TEXT_MUTED)
        screen.blit(title, (rect.x + 30, rect.y + 28))
        screen.blit(subtitle, (rect.x + 30, rect.y + 78))

    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
