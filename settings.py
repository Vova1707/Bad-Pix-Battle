import pygame

class Settings:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((50, 800), (600, 80), 'На главную страницу', 0, lambda:
        self.parent.restart_surface('menu'))
        self.parent.create_button((50, 600), (600, 80), 'Включить звук', 0, self.parent.music_on)
        self.parent.create_button((50, 700), (600, 80), 'Выключить звук', 0, self.parent.music_off)

    def listen(self):
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"),
                                                       (1600, 1000)),
                                (0, 0))
        self.parent.create_text(f'Настройки', 100, (350, 20), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Управление', 50, (500, 150), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'WASD - Передвижение', 24, (80, 250), (255, 0, 0), (200, 100, 50))
        self.parent.create_text(f'F - Стрельба', 24, (80, 300), (255, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Стрелочки - выбор инвертаря', 24, (80, 350), (255, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Правая кнопка мыши - ломание блока', 24, (80, 400), (255, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Левая кнопка мыши - поставить блок', 24, (80, 450), (255, 0, 0), (200, 100, 50))

    def listen_event(self, event):
        pass