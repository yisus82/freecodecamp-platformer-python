from os.path import join
from random import choice, randint

import pygame

from block import Block
from player import Player


class Game:
    FPS = 60
    GRAVITY = 1
    MAX_GRAVITY = 30
    BLOCK_WIDTH = 96
    BLOCK_HEIGHT = 96
    PLAYER_WIDTH = 32
    PLAYER_HEIGHT = 32
    SCROLL_AREA_WIDTH = 200
    BG_COLORS = ["blue", "brown", "gray", "green", "pink", "purple", "yellow"]
    PLAYER_NAMES = ["mask_dude", "ninja_frog", "pink_man", "virtual_guy"]

    def create_background(self):
        image = pygame.image.load(
            join("assets", "background", self.background_color + ".png"))
        _, _, width, height = image.get_rect()
        tiles = []
        for x in range(self.screen.get_width() // width + 1):
            for y in range(self.screen.get_height() // height + 1):
                tiles.append((image, (x * width, y * height)))
        return tiles

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PyPlatformer")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.background_color = choice(self.BG_COLORS)
        self.background = self.create_background()
        self.block_type = randint(0, 2)
        self.clock = pygame.time.Clock()
        self.floor = [Block(i * self.BLOCK_WIDTH, self.screen.get_height() - self.BLOCK_HEIGHT, self, self.block_type)
                      for i in range(-self.screen.get_width() // self.BLOCK_WIDTH, (self.screen.get_width() * 2) // self.BLOCK_WIDTH)]
        self.blocks = []
        self.blocks.append(Block(100, 300, self, 2))
        self.blocks.append(Block(300, 500, self, 2))
        self.blocks.append(Block(500, 800, self, 2))
        self.blocks.append(
            Block(0, self.screen.get_height() - self.BLOCK_HEIGHT * 2, self, 1))
        self.obstacles = [*self.floor, *self.blocks]
        self.player = Player(100, 100, self,
                             choice(self.PLAYER_NAMES), self.obstacles)
        self.offset_x = 0

    def draw_background(self):
        for image, position in self.background:
            self.screen.blit(image, position)

    def draw_floor(self):
        for block in self.floor:
            block.draw()

    def draw_blocks(self):
        for block in self.blocks:
            block.draw()

    def draw(self):
        self.draw_background()
        self.draw_floor()
        self.draw_blocks()
        self.player.draw()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.exit_game()
            self.player.update()
            if ((self.player.rect.right - self.offset_x >= self.screen.get_width() - self.SCROLL_AREA_WIDTH) and self.player.velocity.x > 0) or (
                    (self.player.rect.left - self.offset_x <= self.SCROLL_AREA_WIDTH) and self.player.velocity.x < 0):
                self.offset_x += self.player.velocity.x
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def exit_game(self):
        pygame.quit()
        quit()
