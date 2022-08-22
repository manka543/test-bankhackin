import pygame


class TextBox:
    def __init__(self, surface, x, y, width, height):
        self.surface = surface
        self.active = False
        self.rect = pygame.Rect(x, y, width, height)
        self.cursor = pygame.Rect(x + 12, y + 12, 5, 48)
        self.x = x
        self.y = y
        self.text = ""
        self.font = pygame.font.Font('freesansbold.ttf', 48)
        self.textRender = self.renderText()

    def draw(self, time):
        pygame.draw.rect(self.surface, (255, 255, 255), self.rect, border_radius=3)
        self.surface.blit(self.textRender, (self.x + 10, self.y + 12))
        if self.active and round(time/1000) % 2 == 0:
            self.cursor.x = self.x + 10 + self.textRender.get_width()
            pygame.draw.rect(self.surface, (0, 0, 0), self.cursor)

    def renderText(self):
        return self.font.render(self.text, True, (0, 0, 0))

    def service(self, event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return "enter"
            elif event.unicode.isprintable():
                self.text += event.unicode
            self.textRender = self.renderText()
            return None

    def reset(self):
        self.text = ""
        self.textRender = self.renderText()
        self.active = False
