import pygame
import numpy as np
from client import Client

HOST, PORT = "localhost", 12220

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, img, img_1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"Images/Players/player_1/player_1_{img}_{img_1}.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def move(self):
        pass


class Game:
    def __init__(self, parent):
        self.parent = parent
        self.vvv = 0
        self.screen = parent.screen
        self.comands = {
            pygame.KEYDOWN:
                {(pygame.K_RIGHT, pygame.K_d): lambda: self.client.move("right"),
                 (pygame.K_LEFT, pygame.K_a): lambda: self.client.move("left"),
                 (pygame.K_UP, pygame.K_s): lambda: self.client.move("up"),
                 (pygame.K_DOWN, pygame.K_d): lambda: self.client.move("down"),
                 }}

    def create_widgets(self):
        self.client = Client((HOST, PORT))
        self.parent.create_button((700, 0), (300, 150), 'Выйти', 0, self.close_game)


    def listen(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        self.key = pygame.key.get_pressed()

        gf = {pygame.K_RIGHT: lambda: self.client.move("right"),
              pygame.K_LEFT: lambda: self.client.move("left"),
              pygame.K_UP: lambda: self.client.move("up"),
              pygame.K_DOWN: lambda: self.client.move("down"),
              }
        self.d = 0
        for i in gf.keys():
            if self.key[i]:
                gf[i]()
                self.d = 1
        if not self.d:
            self.vvv += 1
        else:
            self.vvv = 0

        if self.vvv > 10:
            self.client.stoping()

        self.screen.fill((255, 255, 255))
        for i in self.client.players:
            player = Player((i["x"], i["y"]), i["left_right"], i['is_moving'])
            self.screen.blit(player.image, player.rect)

        for i in range(10):
            for j in range(10):
                if self.pole[j][i]:
                    pygame.draw.rect(self.screen, (0, 255, 0),
                                     (i * 100, j * 100, 100, 100))

    def close_game(self):
        self.client.stop = 1
        self.parent.restart_surface('menu')
