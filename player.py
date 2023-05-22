import pygame

from sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y, width, height, game, name):
        super().__init__(x, y, width, height, game,
                         "main_characters", name, animation_speed=0.5)
        self.speed = 5

    def update(self):
        self.animate()
