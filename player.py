from multiprocessing.spawn import old_main_modules

import pygame

from sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y, width, height, game, name):
        super().__init__(x, y, width, height, game,
                         "main_characters", name, animation_speed=0.5)
        self.speed = 5
        self.velocity = pygame.math.Vector2(0, 0)
        self.flip_sprite = False
        self.fall_counter = 0

    def move(self, dx=0, dy=0):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self):
        self.velocity.x = -self.speed
        self.flip_sprite = True

    def move_right(self):
        self.velocity.x = self.speed
        self.flip_sprite = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT or pygame.K_a] and keys[pygame.K_RIGHT or pygame.K_d]:
            self.velocity.x = 0
        elif keys[pygame.K_LEFT or pygame.K_a]:
            self.move_left()
        elif keys[pygame.K_RIGHT or pygame.K_d]:
            self.move_right()
        else:
            self.velocity.x = 0

    def update_status(self):
        old_status = self.status
        if self.velocity.y > 0:
            self.status = "fall"
        elif self.velocity.x != 0:
            self.status = "run"
        else:
            self.status = "idle"
        if old_status != self.status:
            self.frame_index = 0

    def handle_gravity(self):
        self.velocity.y += min(1, (self.fall_counter / self.game.FPS)
                               * self.game.GRAVITY)
        self.fall_counter += 1

    def update(self):
        self.handle_input()
        self.update_status()
        self.handle_gravity()
        self.move(self.velocity.x, self.velocity.y)
        self.animate(self.flip_sprite)
