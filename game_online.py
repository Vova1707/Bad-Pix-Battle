import pygame
import numpy as np
from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN

from player import Player
from client import Client

HOST, PORT = "localhost", 12220


class Game:
    def __init__(self, parent):
        self.parent = parent
        self.vvv = 0
        self.screen = parent.screen
        self.pole = np.array([
            [0] * 10,
            [0] * 10,
            [0] * 10,
            [0] * 10,
            [0] * 10,
            [0] * 10,
            [0] * 10,
            [1] + [0] * 8 + [1],
            [1] * 10,
            [1] * 10])

    def create_widgets(self):
        self.client = Client((HOST, PORT))
        self.parent.create_button((700, 0), (300, 150), 'Выйти', 0, self.close_game)


    def listen(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        self.key = pygame.key.get_pressed()

        gf = {K_RIGHT: lambda: self.client.move("right"),
              K_LEFT: lambda: self.client.move("left"),
              K_UP: lambda: self.client.move("up"),
              K_DOWN: lambda: self.client.move("down"),
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
