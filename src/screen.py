class ScreenManager:


    def __init__(self):

        self.current_screen = "MENU"



    def change_screen(self, screen):

        self.current_screen = screen



    def get_current_screen(self):

        return self.current_screen