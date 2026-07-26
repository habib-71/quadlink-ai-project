import sys
import time
import pygame

from config import (
    SCREEN_WIDTH,
    FPS,
    GAME_TITLE,
    BACKGROUND,
    POP_BOLD,
    POP_REGULAR,
)

from menu import Menu
from screen import ScreenManager
from difficulty import Difficulty

from board import Board
from renderer import BoardRenderer

from ai import AIPlayer
from hard_ai import HardAI



class Game:


    def __init__(self):

        pygame.init()


        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, 720)
        )


        pygame.display.set_caption(
            GAME_TITLE
        )


        self.clock = pygame.time.Clock()



        # Fonts

        self.title_font = pygame.font.Font(
            POP_BOLD,
            56
        )


        self.button_font = pygame.font.Font(
            POP_REGULAR,
            24
        )



        # Screens

        self.screen_manager = ScreenManager()



        # Menu

        self.menu = Menu(
            self.title_font,
            self.button_font
        )



        # Difficulty

        self.difficulty = Difficulty()

        self.selected_difficulty = "Easy"



        # AI

        self.easy_ai = AIPlayer()

        self.hard_ai = HardAI()

        self.ai = self.easy_ai




        # Game

        self.board = Board()

        self.renderer = BoardRenderer()



        # AI Timer

        self.ai_thinking = False

        self.ai_start_time = 0

        self.ai_delay = 1

        self.pending_ai_move = None



        # Result

        self.game_over = False

        self.winner_text = ""



        self.running = True






    def reset_game(self):


        self.board = Board()

        self.game_over = False

        self.winner_text = ""

        self.ai_thinking = False

        self.pending_ai_move = None






    def handle_events(self):


        for event in pygame.event.get():


            if event.type == pygame.QUIT:

                self.running = False




            # Restart

            if event.type == pygame.KEYDOWN:


                if (
                    event.key == pygame.K_r
                    and self.game_over
                ):

                    self.reset_game()





            # Player Move


            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and self.screen_manager.get_current_screen()=="GAME"
                and not self.game_over
                and not self.ai_thinking
            ):


                mouse_x = event.pos[0]


                col = (
                    mouse_x -
                    self.renderer.board_x
                ) // self.renderer.cell_size



                if col in self.board.get_valid_moves():


                    self.board.drop_piece(
                        col,
                        self.board.PLAYER
                    )



                    if self.board.check_winner(
                        self.board.PLAYER
                    ):

                        self.game_over = True

                        self.winner_text = "You Win!"

                        return



                    if self.board.is_full():

                        self.game_over = True

                        self.winner_text = "Draw!"

                        return





                    # AI start


                    self.ai_thinking = True

                    self.ai_start_time = time.time()


                    self.pending_ai_move = (
                        self.ai.get_move(
                            self.board
                        )
                    )









    def update(self):


        current = (
            self.screen_manager
            .get_current_screen()
        )



        # AI Turn


        if self.ai_thinking:


            if (
                time.time()
                -
                self.ai_start_time
                >=
                self.ai_delay
            ):



                if self.pending_ai_move is not None:


                    self.board.drop_piece(
                        self.pending_ai_move,
                        self.board.AI
                    )



                    if self.board.check_winner(
                        self.board.AI
                    ):


                        self.game_over = True

                        self.winner_text = "AI Wins!"



                    elif self.board.is_full():


                        self.game_over = True

                        self.winner_text = "Draw!"




                self.ai_thinking = False

                self.pending_ai_move = None





        # MENU


        if current == "MENU":


            self.menu.update()


            choice = self.menu.handle_click()



            if choice == "Exit":

                self.running = False



            elif choice == "Human vs AI":


                self.screen_manager.change_screen(
                    "DIFFICULTY"
                )






        # DIFFICULTY


        elif current == "DIFFICULTY":


            choice = self.difficulty.handle_click()



            if choice:


                self.selected_difficulty = choice



                if choice == "Easy":

                    self.ai = self.easy_ai



                elif choice == "Hard":

                    self.ai = self.hard_ai




                self.reset_game()


                self.screen_manager.change_screen(
                    "GAME"
                )








        # BACK


        elif current == "GAME":


            mouse = pygame.mouse.get_pos()

            click = pygame.mouse.get_pressed()[0]


            if (
                mouse[0] < 160
                and mouse[1] < 100
                and click
            ):

                self.screen_manager.change_screen(
                    "MENU"
                )








    def draw(self):


        self.screen.fill(
            BACKGROUND
        )


        current = (
            self.screen_manager
            .get_current_screen()
        )



        if current == "MENU":


            self.menu.draw(
                self.screen
            )




        elif current == "DIFFICULTY":


            self.difficulty.draw(
                self.screen
            )




        elif current == "GAME":


            self.renderer.draw(
                self.screen,
                self.board
            )

            if (
                not self.game_over
                and not self.ai_thinking
            ):
                mouse_x = pygame.mouse.get_pos()[0]

                self.renderer.draw_hover_piece(
                    self.screen,
                    mouse_x,
                    self.board
                )


            self.draw_back_button()



            if self.ai_thinking:


                font = pygame.font.Font(
                    POP_REGULAR,
                    30
                )


                text = font.render(
                    "AI Thinking...",
                    True,
                    (37,99,235)
                )


                self.screen.blit(
                    text,
                    (420,650)
                )





            if self.game_over:


                font = pygame.font.Font(
                    POP_BOLD,
                    45
                )


                text = font.render(
                    self.winner_text,
                    True,
                    (37,99,235)
                )


                self.screen.blit(
                    text,
                    (430,600)
                )



                small = pygame.font.Font(
                    POP_REGULAR,
                    25
                )


                restart = small.render(
                    "Press R Restart",
                    True,
                    (0,0,0)
                )


                self.screen.blit(
                    restart,
                    (430,660)
                )



        pygame.display.flip()







    def draw_back_button(self):


        pygame.draw.rect(
            self.screen,
            (37,99,235),
            (40,40,120,45),
            border_radius=12
        )


        font = pygame.font.Font(
            POP_REGULAR,
            22
        )


        text = font.render(
            "< Back",
            True,
            (255,255,255)
        )


        self.screen.blit(
            text,
            (
                40+(120-text.get_width())//2,
                40+(45-text.get_height())//2
            )
        )







    def run(self):


        while self.running:


            self.handle_events()

            self.update()

            self.draw()


        self.clock.tick(
            FPS
        )


        pygame.quit()

        sys.exit()