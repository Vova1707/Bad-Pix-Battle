import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, img=None, running=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/Players/player_1/player_1_0.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def running(self):
        pass