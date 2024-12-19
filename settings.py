import pygame

class Settings:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((0, 500), (150, 80), 'На главную страницу', 0, lambda: self.parent.restart_surface('menu'))
        self.parent.create_button((0, 600), (150, 80), 'Включить звук', 0, self.parent.music_on)
        self.parent.create_button((0, 700), (150, 80), 'Выключить звук', 0, self.parent.music_off)

    def listen(self):
            self.parent.screen.fill((200, 100, 50))
            self.parent.create_text(f'Настройки', 100, (300, 20), (0, 0, 0), (200, 100, 50))
            self.parent.create_text(f'Имя: {self.parent.user[1]}', 24, (50, 150), (0, 0, 0), (200, 100, 50))
            self.parent.create_text(f'Логин: {self.parent.user[2]}', 24, (50, 200), (0, 0, 0), (200, 100, 50))
            self.parent.create_text(f'Побед: 0', 24, (50, 250), (0, 0, 0), (200, 100, 50))
            self.parent.create_text(f'Поражения: 0', 24, (50, 300), (0, 0, 0), (200, 100, 50))
            self.parent.create_text(f'Ничья: 0', 24, (50, 350), (0, 0, 0), (200, 100, 50))