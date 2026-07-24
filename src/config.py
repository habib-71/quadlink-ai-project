"""
QuadLink Configuration
"""

import os

# Window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
GAME_TITLE = "QuadLink"

# Colors (Light Theme)
BACKGROUND = (248, 249, 250)
TEXT_COLOR = (33, 37, 41)
BOARD_BLUE = (37, 99, 235)
RED = (239, 68, 68)
YELLOW = (250, 204, 21)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")

POP_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
POP_REGULAR = os.path.join(FONT_DIR, "Poppins-Regular.ttf")