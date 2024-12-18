import pygame

class Game_Over:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((500, 500), (150, 150), 'На главную страницу', 0, lambda: self.parent.restart_surface('menu'))

    def listen(self):
            self.parent.screen.fill((200, 100, 50))
            self.parent.create_text('Вы проиграли', 24, (400, 400), (0, 0, 0), (200, 100, 50))