import pygame

class Menu:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_buttons((50, 350), (500, 600), (1, 4),
                     ('игра по сети', 'игра оффлайн', 'настройки', 'выйти'),
                     (lambda: self.parent.restart_surface('game'),
                      lambda: print('2'),
                      lambda: self.parent.restart_surface('settings'),
                      lambda: self.parent.restart_surface('registration')))
        self.parent.create_textbox((50, 225), (400, 100))
        self.parent.create_button((460, 230),
                                  (300, 80), 'Изменить', 0,
                                  lambda: self.parent.rename_user(''.join(self.parent.widgets[1].text)))

    def listen(self):
            self.parent.screen.fill((200, 100, 50))
            img = pygame.image.load("Images/Main_menu/main_menu.JPEG").convert()
            self.parent.screen.blit(img, (0, 0))
            self.parent.create_text(f'Здравствуйте, {self.parent.user[1]}', 40, (50, 100), (0, 0, 0), (200, 100, 50))
