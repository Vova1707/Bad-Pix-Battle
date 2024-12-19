import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, img, img_1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"Images/Players/player_1/player_1_{img}_{img_1}.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def running(self):
        pass