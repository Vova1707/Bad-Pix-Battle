import pygame

class Rating:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self):
        self.parent.create_button((50, 800), (600, 80), 'На главную страницу', 0, lambda:
        self.parent.restart_surface('menu'))
        self.parent.create_textbox((50, 200), (400, 100))
        self.parent.create_button((460, 210),
                                  (300, 80), 'Изменить', 0,
                                  lambda: self.parent.rename_user(''.join(self.parent.widgets[1].text)))


    def listen(self):
        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/Game_Menu.jpg"),
                                                       (1600, 1000)),
                                (0, 0))
        self.parent.create_text(f'Профиль', 100, (500, 20), (0, 0, 0), (200, 100, 50))

        self.parent.screen.blit(pygame.transform.scale(pygame.image.load(f"Images/Fon/steve.png"),
                                                       (700, 700)),
                                (800, 200))

        self.parent.create_text(f'Измените имя:', 24, (50, 150), (0, 0, 0), (200, 100, 50))

        self.parent.create_text(f'Имя: {self.parent.user[1]}', 24, (50, 350), (200, 20, 80), (200, 100, 50))
        self.parent.create_text(f'Логин: {self.parent.user[2]}', 24, (50, 400), (200, 20, 80), (200, 100, 50))

        self.parent.create_text(f'Достижения', 24, (500, 400), (255, 100, 200), (200, 100, 50))

        self.parent.create_text(f'Онлайн режим', 24, (50, 500), (0, 255, 255), (200, 100, 50))

        self.parent.create_text(f'Побед: {self.parent.user[4]}', 24, (50, 550), (0, 255, 100), (200, 100, 50))
        self.parent.create_text(f'Поражения: {self.parent.user[6]}', 24, (50, 600), (255, 0, 0), (200, 100, 50))
        self.parent.create_text(f'Ничья: {self.parent.user[5]}', 24, (50, 650), (255, 255, 50), (200, 100, 50))
        self.parent.create_text(f'Уровни: {self.parent.user[7]}', 24, (50, 700), (255, 55, 50), (200, 100, 50))

        left = 0
        down = 0

        for i in range(8, 13):
            if self.parent.user[i]:
                self.parent.screen.blit(
                    pygame.transform.scale(pygame.image.load(f"Images/Object/{i - 7}.png"), (70, 140)),
                    (500 + left, 480 + down))
                if left - down == 160:
                    down = 150
                    left = 0
                else:
                    left += 80

        self.parent.screen.blit(
            pygame.transform.scale(pygame.image.load(f"Images/Fon/алмаз.png"), (50, 50)),
            (50, 740))
        self.parent.create_text(f': {self.parent.user[13]}', 24, (110, 750), (0, 0, 0), (200, 100, 50))



    def listen_event(self, event):
        pass