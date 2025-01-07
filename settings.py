import pygame

class Settings:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((100, 500), (600, 80), 'На главную страницу', 0, lambda: self.parent.restart_surface('menu'))
        self.parent.create_button((100, 600), (600, 80), 'Включить звук', 0, self.parent.music_on)
        self.parent.create_button((100, 700), (600, 80), 'Выключить звук', 0, self.parent.music_off)

    def listen(self):
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"), (1600, 1000)),
                                (0, 0))
        self.parent.create_text(f'Настройки', 100, (300, 20), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'WASD - Передвижение', 24, (50, 150), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'F - Стрельба', 24, (50, 200), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Стрелочки - выбор инвертаря', 24, (50, 250), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Правая кнопка мыши - ломание блока', 24, (50, 300), (0, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Левая кнопка мыши - поставить блок', 24, (50, 350), (0, 0, 0), (200, 100, 50))

    def listen_event(self, event):
        pass