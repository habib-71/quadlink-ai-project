"""Shared QuadLink display configuration and visual theme."""

import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
FPS = 60
GAME_TITLE = "QuadLink"

# Modern navy-and-indigo interface palette.
BACKGROUND = (12, 19, 38)
BACKGROUND_TOP = (20, 32, 62)
SURFACE = (24, 36, 66)
SURFACE_LIGHT = (32, 48, 85)
SURFACE_BORDER = (67, 89, 137)
TEXT_COLOR = (236, 242, 255)
TEXT_MUTED = (160, 177, 211)
PRIMARY = (99, 102, 241)
PRIMARY_HOVER = (129, 130, 255)
PRIMARY_DARK = (72, 71, 190)
BOARD_BLUE = (49, 70, 154)
BOARD_DARK = (35, 49, 115)
RED = (244, 92, 112)
RED_LIGHT = (255, 139, 151)
YELLOW = (250, 194, 75)
YELLOW_LIGHT = (255, 221, 122)
WHITE = (245, 248, 255)
BLACK = (7, 11, 24)
SUCCESS = (75, 207, 151)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")
POP_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
POP_REGULAR = os.path.join(FONT_DIR, "Poppins-Regular.ttf")
