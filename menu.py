import pygame

class Menu:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_buttons((50, 350), (500, 600), (1, 4),
                     ('игра по сети', 'игра оффлайн', 'профиль', 'настройки'),
                     (lambda: self.parent.restart_surface('game_online_menu'),
                      lambda: self.parent.restart_surface('game_offline'),
                      lambda: self.parent.restart_surface('rating'),
                      lambda: self.parent.restart_surface('settings')))

        self.parent.create_button((1380, 900),
                                  (200, 80), 'выйти', 0,
                                  lambda: self.parent.restart_surface('registration'))

    def listen(self):
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Main_Menu.jpg"),
                                                       (1600, 1000)),
                                (0, 0))
        self.parent.create_text(f'B', 150, (330, 30), (255, 0, 0), (200, 100, 50))
        self.parent.create_text(f'P', 150, (640, 30), (0, 255, 0), (200, 100, 50))
        self.parent.create_text(f'B', 150, (910, 30), (255, 255, 50), (200, 100, 50))
        self.parent.create_text(f'ad  ix  attle', 150, (400, 30), (20, 10, 50), (200, 100, 50))

    def listen_event(self, event):
        pass
