import pygame


class Game:
    FPS = 60

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PyPlatformer")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

    def run(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.exit_game()
            self.clock.tick(self.FPS)
        self.exit_game()

    def exit_game(self):
        pygame.quit()
        quit()
