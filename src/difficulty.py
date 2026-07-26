import pygame

from config import POP_BOLD, POP_REGULAR



class Difficulty:


    def __init__(self):

        self.buttons = {

            "Easy": pygame.Rect(
                400,
                300,
                220,
                70
            ),

            "Hard": pygame.Rect(
                400,
                420,
                220,
                70
            )

        }



    def draw(self, screen):


        title_font = pygame.font.Font(
            POP_BOLD,
            50
        )


        button_font = pygame.font.Font(
            POP_REGULAR,
            28
        )



        title = title_font.render(
            "Select Difficulty",
            True,
            (37,99,235)
        )


        screen.blit(
            title,
            (330,170)
        )



        for name, rect in self.buttons.items():


            pygame.draw.rect(
                screen,
                (37,99,235),
                rect,
                border_radius=15
            )


            text = button_font.render(
                name,
                True,
                (255,255,255)
            )


            screen.blit(
                text,
                (
                    rect.x +
                    (rect.width-text.get_width())//2,

                    rect.y +
                    (rect.height-text.get_height())//2
                )
            )





    def handle_click(self):


        if pygame.mouse.get_pressed()[0]:


            mouse = pygame.mouse.get_pos()


            for name, rect in self.buttons.items():


                if rect.collidepoint(mouse):

                    return name


        return None