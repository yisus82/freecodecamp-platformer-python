import pygame


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.game = game
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        self.game.screen.blit(
            self.image, (self.rect.x - self.game.offset_x, self.rect.y))
