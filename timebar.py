import pygame


class TimeBar:
    screen: pygame.surface.Surface

    def __init__(self, screen, x, y, height, width, time):
        self.screen = screen
        self.time = time
        self.framesToEnd = self.time * 60
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.barWidth = self.width - 6
        self.barX = self.x + 3
        self.frameJump = self.barWidth / 2 / self.framesToEnd

    def draw(self):
        self.framesToEnd -= 1
        self.barWidth -= self.frameJump * 2
        self.barX += self.frameJump
        pygame.draw.rect(self.screen, "black", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, "slateblue4", (self.barX, self.y + 3, self.barWidth, self.height - 6))

    def end(self):
        if self.framesToEnd == 0:
            return True
        else:
            return False

    def reset(self):
        self.framesToEnd = self.time * 60
        self.barWidth = self.width - 6
        self.barX = self.x + 3
