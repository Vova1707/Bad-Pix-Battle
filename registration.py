import pygame


class Registration:
    def __init__(self, parent):
        self.parent = parent
        self.parent.user = None

    def create_widgets(self):
        self.parent.create_textbox((300, 150), (400, 80))
        self.parent.create_textbox((300, 250), (400, 80))
        self.parent.create_button((350, 350),
                                  (300, 80), 'Зарегистрироваться', 0,
                                  lambda: self.parent.log_in(''.join(self.parent.widgets[0].text), ''.join(self.parent.widgets[1].text)))
        self.parent.create_button((350, 450),
                                  (300, 80), 'Войти', 0,
                                  lambda: self.parent.log_up(''.join(self.parent.widgets[0].text), ''.join(self.parent.widgets[1].text)))


    def listen(self):
        self.parent.screen.fill((200, 100, 50))
        self.parent.create_text('Авторизация', 40, (350, 50), (0, 0, 0), (200, 100, 50))
        self.parent.create_text('Введите пароль:', 24, (100, 275), (0, 0, 0), (200, 100, 50))
        self.parent.create_text('Введите логин:', 24, (110, 175), (0, 0, 0), (200, 100, 50))