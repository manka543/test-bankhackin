import pygame


class Button:
    def __init__(self, screen, position, size, textsize, caption="Button", color=(0, 0, 0), hover=(20, 20, 20),
                 pressed=(40, 40, 40)):
        self.rect = pygame.rect.Rect(position, size)
        self.color = color
        self.colorHover = hover
        self.colorPressed = pressed
        self.font = pygame.font.Font('freesansbold.ttf', textsize)
        self.text = self.font.render(caption, True, (255, 255, 255))
        self.screen = screen

    def draw(self, mousepos, ispressed):
        if self.rect.collidepoint(mousepos) and ispressed:
            pygame.draw.rect(self.screen, self.colorPressed, self.rect)
        elif self.rect.collidepoint(mousepos):
            pygame.draw.rect(self.screen, self.colorHover, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.text, (self.rect.centerx - self.text.get_width() / 2, self.rect.y + 50))

    def isClicked(self, mousepos, isclicked):
        if self.rect.collidepoint(mousepos) and isclicked:
            return True
        return False
