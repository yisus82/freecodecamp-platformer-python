from multiprocessing.spawn import old_main_modules

import pygame

from sprite import Sprite


class Player(Sprite):
    def __init__(self, x, y, game, name, obstacles):
        super().__init__(x, y, game.PLAYER_WIDTH, game.PLAYER_HEIGHT, game,
                         "main_characters", name, animation_speed=0.5)
        self.obstacles = obstacles
        self.speed = 5
        self.velocity = pygame.math.Vector2(0, 0)
        self.flip_sprite = False
        self.grounded = False
        self.jump_force = 15
        self.jump_counter = 0
        self.jumping = False
        self.jump_time = 0
        self.jump_cooldown = 400

    def move(self, dx=0, dy=0):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, running=False):
        if running:
            self.velocity.x = -self.speed * 2
        else:
            self.velocity.x = -self.speed
        self.flip_sprite = True

    def move_right(self, running=False):
        if running:
            self.velocity.x = self.speed * 2
        else:
            self.velocity.x = self.speed
        self.flip_sprite = False

    def jump(self):
        if self.jumping:
            return
        self.jumping = True
        if self.grounded:
            self.velocity.y = -self.jump_force / self.game.GRAVITY
            self.jump_counter = 1
            self.grounded = False
            self.jump_time = pygame.time.get_ticks()
        elif self.jump_counter < 2:
            self.velocity.y = -self.jump_force / self.game.GRAVITY
            self.jump_counter += 1
            self.jump_time = pygame.time.get_ticks()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.velocity.x = 0
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                self.move_left(running=True)
            else:
                self.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                self.move_right(running=True)
            else:
                self.move_right()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump()

    def update_status(self):
        old_status = self.status
        if self.velocity.y > self.game.GRAVITY * 2:
            self.status = "fall"
        elif self.velocity.y < -self.game.GRAVITY * 2:
            self.status = "jump" if self.jump_counter == 1 else "double_jump"
        elif self.velocity.x != 0:
            self.status = "run"
        else:
            self.status = "idle"
        if old_status != self.status:
            self.frame_index = 0

    def handle_gravity(self):
        if not self.grounded:
            self.velocity.y += self.game.GRAVITY
            if self.velocity.y > self.game.MAX_GRAVITY:
                self.velocity.y = self.game.MAX_GRAVITY

    def check_horizontal_collisions(self):
        for obstacle in self.obstacles:
            if pygame.sprite.collide_mask(self, obstacle):
                self.move(-self.velocity.x, 0)
                break

    def check_vertical_collisions(self):
        self.grounded = False
        for obstacle in self.obstacles:
            if pygame.sprite.collide_mask(self, obstacle):
                if self.velocity.y > 0:
                    self.rect.bottom = obstacle.rect.top
                    self.velocity.y = 0
                    self.grounded = True
                    self.jump_counter = 0
                elif self.velocity.y < 0:
                    self.rect.top = obstacle.rect.bottom
                    self.velocity.y = -self.velocity.y

    def handle_cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.jumping and current_time - self.jump_time > self.jump_cooldown:
            self.jumping = False

    def update(self):
        self.handle_gravity()
        self.handle_cooldowns()
        self.handle_input()
        self.move(self.velocity.x, self.velocity.y)
        self.check_horizontal_collisions()
        self.check_vertical_collisions()
        self.update_status()
        self.animate(self.flip_sprite)
