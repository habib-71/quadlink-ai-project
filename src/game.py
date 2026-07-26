import math
import sys
import time

import pygame

from ai import AIPlayer
from audio import AudioManager
from board import Board
from config import BACKGROUND, BACKGROUND_TOP, FPS, GAME_TITLE, POP_BOLD, POP_REGULAR, SCREEN_HEIGHT, SCREEN_WIDTH, SUCCESS, TEXT_COLOR, TEXT_MUTED
from difficulty import Difficulty
from hard_ai import HardAI
from menu import Menu
from renderer import BoardRenderer
from screen import ScreenManager
from settings import Settings
from statistics import GameStats, Statistics
from ui import Button, draw_card


class Game:
    """Coordinates the existing game logic and the presentation layer."""

    DROP_ACCELERATION = 7200
    DROP_MAX_SPEED = 1250

    def __init__(self):
        # Request a predictable PCM format for generated fallback effects.
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.background_surface = self.build_background()
        self.audio = AudioManager()

        self.title_font = pygame.font.Font(POP_BOLD, 56)
        self.button_font = pygame.font.Font(POP_REGULAR, 20)
        self.heading_font = pygame.font.Font(POP_BOLD, 30)
        self.info_font = pygame.font.Font(POP_REGULAR, 17)
        self.result_font = pygame.font.Font(POP_BOLD, 42)

        self.screen_manager = ScreenManager()
        self.menu = Menu(self.title_font, self.button_font)
        self.difficulty = Difficulty()
        self.settings = Settings()
        self.stats = GameStats()
        self.statistics = Statistics(self.stats)
        self.selected_difficulty = "Easy"
        self.game_mode = "AI"
        self.active_player = Board.PLAYER
        self.animation_enabled = True
        self.easy_ai = AIPlayer()
        self.hard_ai = HardAI()
        self.ai = self.easy_ai

        self.board = Board()
        self.renderer = BoardRenderer()
        self.back_button = Button(36, 30, 118, 42, "←  Menu", self.info_font)

        self.ai_thinking = False
        self.ai_start_time = 0
        self.ai_delay = 1
        self.pending_ai_move = None
        self.falling_piece = None
        self.game_over = False
        self.winner_text = ""
        self.running = True

        self.transition_target = None
        self.transition_alpha = 0.0
        self.transition_direction = 0
        self.wait_for_release = False
        self.elapsed_time = 0.0

    def reset_game(self):
        self.board = Board()
        self.game_over = False
        self.winner_text = ""
        self.ai_thinking = False
        self.pending_ai_move = None
        self.falling_piece = None
        self.active_player = self.board.PLAYER

    def request_screen(self, screen):
        if self.transition_target is None and screen != self.screen_manager.get_current_screen():
            self.transition_target = screen
            self.transition_direction = 1
            self.transition_alpha = 0.0

    def update_transition(self, delta_time):
        if self.transition_direction == 0:
            return
        self.transition_alpha += self.transition_direction * 780 * delta_time
        if self.transition_direction > 0 and self.transition_alpha >= 255:
            self.transition_alpha = 255
            self.screen_manager.change_screen(self.transition_target)
            self.transition_target = None
            self.transition_direction = -1
            self.wait_for_release = True
        elif self.transition_direction < 0 and self.transition_alpha <= 0:
            self.transition_alpha = 0
            self.transition_direction = 0

    def start_drop(self, col, player):
        row = self.board.get_drop_row(col)
        if row == -1:
            return False
        _, target_y = self.renderer.get_cell_center(row, col)
        self.falling_piece = {
            "col": col,
            "player": player,
            "current_y": self.renderer.board_y - 46,
            "target_y": target_y,
            "speed": 0.0,
        }
        if not self.animation_enabled:
            self.finish_drop()
        return True

    def finish_drop(self):
        piece = self.falling_piece
        self.falling_piece = None
        if piece is None:
            return
        self.board.drop_piece(piece["col"], piece["player"])
        self.stats.record_move()
        self.audio.play("drop")

        if self.board.check_winner(piece["player"]):
            self.game_over = True
            if self.game_mode == "PVP":
                number = 1 if piece["player"] == self.board.PLAYER else 2
                self.winner_text = f"Player {number} wins!"
                self.audio.play("win")
            else:
                self.winner_text = "You win!" if piece["player"] == self.board.PLAYER else "AI wins"
                self.audio.play("win" if piece["player"] == self.board.PLAYER else "lose")
            self.ai_thinking = False
            self.pending_ai_move = None
            self.stats.record_result(self.game_mode, piece["player"])
            return
        if self.board.is_full():
            self.game_over = True
            self.winner_text = "It’s a draw"
            self.audio.play("draw")
            self.ai_thinking = False
            self.pending_ai_move = None
            self.stats.record_result(self.game_mode)
            return
        if self.game_mode == "PVP":
            self.active_player = self.board.AI if piece["player"] == self.board.PLAYER else self.board.PLAYER
        elif piece["player"] == self.board.PLAYER:
            self.ai_thinking = True
            self.ai_start_time = time.time()
            self.pending_ai_move = self.ai.get_move(self.board)
        else:
            self.ai_thinking = False
            self.pending_ai_move = None

    def update_drop_animation(self, delta_time):
        if self.falling_piece is None:
            return
        piece = self.falling_piece
        piece["speed"] = min(piece["speed"] + self.DROP_ACCELERATION * delta_time, self.DROP_MAX_SPEED)
        piece["current_y"] += piece["speed"] * delta_time
        if piece["current_y"] >= piece["target_y"]:
            piece["current_y"] = piece["target_y"]
            self.finish_drop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
                self.reset_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                current = self.screen_manager.get_current_screen()
                if current == "MENU" and any(button.rect.collidepoint(event.pos) for button in self.menu.buttons):
                    self.audio.play("click")
                elif current == "DIFFICULTY" and any(card.rect.collidepoint(event.pos) for card in self.difficulty.cards.values()):
                    self.audio.play("click")
                elif current == "GAME" and self.back_button.rect.collidepoint(event.pos):
                    self.audio.play("click")
                elif current == "SETTINGS" and (
                    any(button.rect.collidepoint(event.pos) for button in self.settings.toggle_buttons.values())
                    or self.settings.back_button.rect.collidepoint(event.pos)
                ):
                    self.audio.play("click")
                elif current == "STATISTICS" and (
                    self.statistics.reset_button.rect.collidepoint(event.pos)
                    or self.statistics.back_button.rect.collidepoint(event.pos)
                ):
                    self.audio.play("click")
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and self.screen_manager.get_current_screen() == "GAME"
                and not self.game_over
                and not self.ai_thinking
                and self.falling_piece is None
                and self.transition_direction == 0
            ):
                col = (event.pos[0] - self.renderer.board_x) // self.renderer.cell_size
                if col in self.board.get_valid_moves():
                    player = self.active_player if self.game_mode == "PVP" else self.board.PLAYER
                    self.start_drop(col, player)

    def update(self, delta_time):
        self.elapsed_time += delta_time
        self.update_transition(delta_time)
        current = self.screen_manager.get_current_screen()
        if self.wait_for_release and not pygame.mouse.get_pressed()[0]:
            self.wait_for_release = False

        if current == "MENU":
            self.menu.update(delta_time)
            choice = None if self.wait_for_release else self.menu.handle_click()
            if choice == "Exit":
                self.running = False
            elif choice == "Human vs AI":
                self.game_mode = "AI"
                self.request_screen("DIFFICULTY")
            elif choice == "Human vs Human":
                self.game_mode = "PVP"
                self.reset_game()
                self.request_screen("GAME")
            elif choice == "Settings":
                self.request_screen("SETTINGS")
            elif choice == "Statistics":
                self.request_screen("STATISTICS")

        elif current == "DIFFICULTY":
            self.difficulty.update(delta_time)
            choice = None if self.wait_for_release else self.difficulty.handle_click()
            if choice:
                self.selected_difficulty = choice
                self.ai = self.easy_ai if choice == "Easy" else self.hard_ai
                self.reset_game()
                self.request_screen("GAME")

        elif current == "SETTINGS":
            self.settings.update(delta_time)
            choice = None if self.wait_for_release else self.settings.handle_click()
            if choice:
                if choice == "back":
                    self.request_screen("MENU")
                else:
                    self.audio.set_sound_enabled(self.settings.values["sound"])
                    self.audio.set_music_enabled(self.settings.values["music"])
                    self.animation_enabled = self.settings.values["animation"]

        elif current == "STATISTICS":
            self.statistics.update(delta_time)
            choice = None if self.wait_for_release else self.statistics.handle_click()
            if choice == "back":
                self.request_screen("MENU")

        elif current == "GAME":
            mouse = pygame.mouse.get_pos()
            pressed = pygame.mouse.get_pressed()[0]
            self.back_button.update(mouse, pressed, delta_time)
            self.renderer.update_hover(mouse[0], self.board, delta_time)
            self.update_drop_animation(delta_time)
            if self.back_button.clicked(mouse, pressed) and self.transition_direction == 0 and not self.wait_for_release:
                self.request_screen("MENU")

            if self.ai_thinking and self.falling_piece is None and time.time() - self.ai_start_time >= self.ai_delay:
                if self.pending_ai_move is not None:
                    self.start_drop(self.pending_ai_move, self.board.AI)
                else:
                    self.ai_thinking = False

    def draw_background(self):
        self.screen.blit(self.background_surface, (0, 0))

    def build_background(self):
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            blend = y / SCREEN_HEIGHT
            color = tuple(int(a + (b - a) * blend) for a, b in zip(BACKGROUND_TOP, BACKGROUND))
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        return surface

    def draw_game_header(self):
        title = self.heading_font.render("QuadLink", True, TEXT_COLOR)
        subtitle_text = "Player vs Player" if self.game_mode == "PVP" else f"{self.selected_difficulty} difficulty"
        subtitle = self.info_font.render(subtitle_text, True, TEXT_MUTED)
        self.screen.blit(title, (188, 31))
        self.screen.blit(subtitle, (190, 67))
        self.back_button.draw(self.screen)

        if self.game_over:
            status = "Game complete"
            color = SUCCESS
        elif self.game_mode == "PVP":
            player_number = 1 if self.active_player == self.board.PLAYER else 2
            status = f"Player {player_number}'s turn"
            color = (244, 92, 112) if player_number == 1 else (250, 194, 75)
        elif self.ai_thinking:
            dots = "." * (1 + int(self.elapsed_time * 3) % 3)
            status = f"AI is thinking{dots}"
            color = (250, 194, 75)
        else:
            status = "Your turn"
            color = (244, 92, 112)
        pill = pygame.Rect(914, 41, 246, 42)
        draw_card(self.screen, pill, radius=21, shadow=False)
        indicator = pygame.Rect(pill.x + 14, pill.y + 14, 14, 14)
        pygame.draw.circle(self.screen, color, indicator.center, 7)
        text = self.info_font.render(status, True, TEXT_COLOR)
        self.screen.blit(text, (pill.x + 40, pill.y + (pill.height - text.get_height()) // 2))

    def draw_result(self):
        pulse = 1 + 0.025 * math.sin(self.elapsed_time * 5)
        rect = pygame.Rect(0, 0, int(430 * pulse), int(148 * pulse))
        rect.center = (SCREEN_WIDTH // 2, 398)
        draw_card(self.screen, rect, radius=24)
        result = self.result_font.render(self.winner_text, True, TEXT_COLOR)
        hint = self.info_font.render("Press R to start another game", True, TEXT_MUTED)
        self.screen.blit(result, result.get_rect(center=(rect.centerx, rect.y + 58)))
        self.screen.blit(hint, hint.get_rect(center=(rect.centerx, rect.y + 105)))

    def draw(self):
        self.draw_background()
        current = self.screen_manager.get_current_screen()
        if current == "MENU":
            self.menu.draw(self.screen)
        elif current == "DIFFICULTY":
            self.difficulty.draw(self.screen)
        elif current == "SETTINGS":
            self.settings.draw(self.screen)
        elif current == "STATISTICS":
            self.statistics.draw(self.screen)
        elif current == "GAME":
            self.draw_game_header()
            self.renderer.draw(self.screen, self.board)
            if self.falling_piece is not None:
                self.renderer.draw_falling_piece(self.screen, self.falling_piece["col"], self.falling_piece["current_y"], self.falling_piece["player"])
            if not self.game_over and not self.ai_thinking and self.falling_piece is None:
                player = self.active_player if self.game_mode == "PVP" else self.board.PLAYER
                self.renderer.draw_hover_piece(self.screen, pygame.mouse.get_pos()[0], self.board, player)
            if self.game_over:
                self.draw_result()

        if self.transition_alpha > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((7, 11, 24, int(self.transition_alpha)))
            self.screen.blit(overlay, (0, 0))
        pygame.display.flip()

    def run(self):
        while self.running:
            delta_time = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.handle_events()
            self.update(delta_time)
            self.draw()
        pygame.quit()
        sys.exit()
