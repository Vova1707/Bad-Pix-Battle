import pygame
from player import Player
from client import Client


HOST, PORT = "localhost", 12000
pygame.init()
WINDOW_HEIGHT, WINDOW_WEIGHT = 1000, 1000


class Bad_Pix_Battle:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WEIGHT))
        self.client = Client((HOST, PORT))
        self.clock = pygame.time.Clock()
        self.view_logo()
        self.listen_main_game()
        self.RUN = True

    def menu(self):
        """
        Отвечает за прорисовку меню
        """
        arrow_right = pygame.image.load('Images/Main_menu/arrow_right.png')
        arrow_left = pygame.image.load('Images/Main_menu/arrow_left.png')
        arrow_pos_left = [(125, 275 + i * 300) for i in range(4)]
        arrow_pos_right = [(825, 275 + i * 300) for i in range(4)]
        i_a = 0
        menu_surface = pygame.image.load('Images/Main_menu/Menu.png')
        while self.RUN:
            for e in pygame.event.get():
                if e.key == pygame.K_DOWN:
                    i_a += 1
                    if i_a >= 3:
                        i_a = 0
                    pygame.time.delay(30)
                if e.key == pygame.K_UP:
                    i_a -= 1
                    if i_a < 0:
                        i_a = 3
                    pygame.time.delay(30)

                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        donne = False
                    elif e.key == pygame.K_RETURN:
                        if i_a == 0:
                            # Окно сообщений
                            self.show_message_frame = not self.show_message_frame
                        elif i_a == 1:
                            # Свечение
                            self.show_glow = not self.show_glow
                        elif i_a == 2:
                            # Сохранить
                            com = self.save()
                            if com != 'OK':
                                return com
                        elif i_a == 3:
                            # Загрузить
                            return 'LOAD'
                        elif i_a == 4:
                            # Титры
                            pass
                        elif i_a == 5:
                            # Выход
                            self.RUN = False
                            return 'QUIT'

            self.screen.fill((0, 0, 0))
            self.screen.blit(menu_surface, (0, 0))
            self.screen.blit(arrow_right, arrow_pos_right[i_a])
            self.screen.blit(arrow_left, arrow_pos_left[i_a])
            pygame.display.flip()

    def view_logo(self):
        """
        Показ логотипа на 2 секунды
        """
        logo = pygame.image.load('ааав.jpeg')
        self.screen.fill((255, 255, 255))
        self.screen.blit(logo, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)

    def listen_main_game(self):
        while True:
            for event in pygame.event.get():  # Перебираем все события которые произошли с программой
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('a'):
                        self.client.move("left")
                    if event.key == ord('d'):
                        self.client.move("right")
                    if event.key == ord('w'):
                        self.client.move("up")
                    if event.key == ord('s'):
                        self.client.move("down")

                if event.type == pygame.QUIT:  # Проверяем на выход из игры
                    self.client.sock.close()
                    exit()
            self.screen.fill((0, 0, 0))

            for i in self.client.players:
                print(i)
                player = Player((i["x"], i["y"]))
                self.screen.blit(player.image, player.rect)
            pygame.display.update()

            self.clock.tick(60)




if __name__ == "__main__":
    Bad_Pix_Battle().__init__()