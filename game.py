from os.path import join
from random import choice

import pygame


class Game:
    FPS = 60
    BG_COLORS = ["blue", "brown", "gray", "green", "pink", "purple", "yellow"]

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
        self.clock = pygame.time.Clock()

    def draw_background(self):
        for image, position in self.background:
            self.screen.blit(image, position)

    def draw(self):
        self.draw_background()
        pygame.display.update()

    def run(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.exit_game()
            self.draw()
            self.clock.tick(self.FPS)
        self.exit_game()

    def exit_game(self):
        pygame.quit()
        quit()
