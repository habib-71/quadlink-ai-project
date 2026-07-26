import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from settings import Settings


def test_settings_volume_is_clamped_and_clickable():
    pygame.init()
    settings = Settings(volume=3)
    assert settings.values["volume"] == 1.0
    assert settings.handle_click((settings.volume_rect.x, settings.volume_rect.centery)) == "volume"
    assert settings.values["volume"] == 0.0
    pygame.quit()
