from os import listdir
from os.path import isfile, join

import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game, category, name, initial_status="idle", animation_speed=0):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.game = game
        self.category = category
        self.name = name
        self.status = initial_status
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.animations = self.load_animations()
        self.image = self.animations[self.status][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

    def load_animations(self):
        path = join("assets", self.category, self.name)
        images = [filename for filename in listdir(
            path) if isfile(join(path, filename))]
        animations = {}
        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
            sprites = []
            for i in range(sprite_sheet.get_width() // self.rect.width):
                surface = pygame.Surface(
                    (self.rect.width, self.rect.height), pygame.SRCALPHA, depth=32)
                rect = pygame.Rect(i * self.rect.width, 0,
                                   self.rect.width, self.rect.height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))
            animations[image.replace(".png", "")] = sprites
        return animations

    def animate(self, flip_sprite=False):
        if self.status in self.animations:
            animation = self.animations[self.status]
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
            self.image = animation[int(self.frame_index)]
            if flip_sprite:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
