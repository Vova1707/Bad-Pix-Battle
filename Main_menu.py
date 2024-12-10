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
        arrow = pygame.image.load('Images/Main_menu/Arrow.png')
        arrow_pos = [(400, 400 + x * 50) for x in range(5)]
        i_a = 0
        menu_surface = pygame.image.load('Images/Main_menu/Menu.png')
        while self.RUN:
            for e in pygame.event.get():
                    if e.key == pygame.K_DOWN:
                        i_a += 1
                        if i_a >= len(arrow_pos):
                            i_a = 0
                        pygame.time.delay(30)
                    if e.key == pygame.K_UP:
                        i_a -= 1
                        if i_a < 0:
                            i_a = len(arrow_pos) - 1
                        pygame.time.delay(30)
            self.screen.fill((0, 0, 0))
            self.screen.blit(menu_surface, (0, 0))
            self.screen.blit(arrow, arrow_pos[i_a])
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