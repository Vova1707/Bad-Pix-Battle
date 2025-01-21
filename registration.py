import pygame


class Registration:
    def __init__(self, parent):
        self.parent = parent
        self.parent.user = None

    def create_widgets(self):
        self.parent.create_textbox((600, 225), (400, 80))
        self.parent.create_textbox((600, 375), (400, 80))
        self.parent.create_button((500, 500),
                                  (600, 80), 'Зарегистрироваться', 0,
                                  lambda: self.parent.log_in(''.join(self.parent.widgets[0].text),
                                                             ''.join(self.parent.widgets[1].text)))
        self.parent.create_button((650, 600),
                                  (300, 80), 'Войти', 0,
                                  lambda: self.parent.log_up(''.join(self.parent.widgets[0].text),
                                                             ''.join(self.parent.widgets[1].text)))


    def listen(self):
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"),
                                                       (1600, 1000)), (0, 0))
        self.parent.create_text('Авторизация', 40, (575, 50), (0, 0, 0), (200, 100, 50))
        self.parent.create_text('Введите пароль:', 24, (550, 325), (0, 0, 0), (200, 100, 50))
        self.parent.create_text('Введите логин:', 24, (550, 175), (0, 0, 0), (200, 100, 50))

    def listen_event(self, event):
        pass