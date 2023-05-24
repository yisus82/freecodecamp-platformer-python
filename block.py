from os.path import join

import pygame

from object import Object


class Block(Object):
    BLOCK_OFFSET_X = 96
    BLOCK_OFFSET_Y = 10
    BLOCK_SPRITE_WIDTH = 50
    BLOCK_SPRITE_HEIGHT = 50

    def __init__(self, x, y, game, block_type=0):
        super().__init__(x, y, game.BLOCK_WIDTH, game.BLOCK_HEIGHT, game)
        self.block_type = block_type
        self.image.blit(self.get_block(), (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    def get_block(self):
        path = join("assets", "terrain", "terrain.png")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(self.BLOCK_OFFSET_X, (self.BLOCK_SPRITE_HEIGHT+self.BLOCK_OFFSET_Y)*self.block_type,
                           self.rect.width, self.rect.height)
        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)
