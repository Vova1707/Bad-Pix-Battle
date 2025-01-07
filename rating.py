import pygame

class Rating:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((100, 500), (600, 80), 'На главную страницу', 0, lambda: self.parent.restart_surface('menu'))


    def listen(self):
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"), (1600, 1000)),
                                (0, 0))
        self.parent.create_text(f'Рейтинг', 100, (300, 20), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Имя: {self.parent.user[1]}', 24, (50, 150), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Логин: {self.parent.user[2]}', 24, (50, 200), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Побед: {self.parent.user[4]}', 24, (50, 250), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Поражения: {self.parent.user[6]}', 24, (50, 300), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Ничья: {self.parent.user[5]}', 24, (50, 350), (0, 0, 0), (200, 100, 50))

    def listen_event(self, event):
        pass