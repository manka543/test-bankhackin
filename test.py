import pygame
import console


class Test:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1275, 760))
        self.console = console.Console(self.screen, 50, 50, 1175, 660, 24, (0, 0, 0), (0, 0, 0))
        self.clock = pygame.time.Clock()
        self.testLoop()

    def testLoop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.console.service(event)
            self.screen.fill((35, 35, 35))
            self.console.draw(pygame.time.get_ticks())
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()


test1 = Test()
