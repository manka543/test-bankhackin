import pygame
from random import randint


def circlePoints(r):
    x, y, d = r, 0, 1 - r
    points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if d < 0:
            d += 2 * y - 1
        else:
            x -= 1
            d += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def renderTextWithBorder(text, font, textcolor, bordercolor, borderwidth):
    textsurface = font.render(text, True, textcolor).convert_alpha()
    width = textsurface.get_width() + 2 * borderwidth
    height = font.get_height()

    borderSurface = pygame.Surface((width, height + 2 * borderwidth)).convert_alpha()
    borderSurface.fill((0, 0, 0, 0))

    surface = borderSurface.copy()

    borderSurface.blit(font.render(text, True, bordercolor).convert_alpha(), (0, 0))

    for dx, dy in circlePoints(borderwidth):
        surface.blit(borderSurface, (dx + borderwidth, dy + borderwidth))

    surface.blit(textsurface, (borderwidth, borderwidth))
    return surface


class Box:
    screen: pygame.surface.Surface
    numberRender: pygame.surface.Surface

    def __init__(self, screen, number, position, fakenumber, colors, shapes):
        self.screen = screen
        self.number = number
        self.position = position
        self.fakeNumber = fakenumber
        self.font = pygame.font.Font('freesansbold.ttf', 180)
        self.textFont = pygame.font.Font('freesansbold.ttf', 30)
        self.fakeNumberFont = pygame.font.Font('freesansbold.ttf', 45)
        self.numberRender = self.font.render(str(self.number), True, (255, 255, 255))
        self._x = self.position * 300 + 63
        self._y = 100
        self.rect = pygame.rect.Rect(self._x, self._y, 250, 250)
        self.borderColors = {"black": "white", "green": "black", "blue": "black", "purple": "black", "yellow": "black",
                             "orange": "black", "red": "black", "white": "black"}
        self.colors2RGB = colors
        self.colors = []
        for keys in colors:
            self.colors.append(keys)
        self.shapes = shapes
        # draw elements of box
        self.shape = self.shapes[randint(0, len(self.shapes) - 1)]
        self.innerShape = self.shapes[randint(0, len(self.shapes) - 1)]
        self.shapeText = self.shapes[randint(0, len(self.shapes) - 1)]
        self.colorText = self.colors[randint(0, len(self.colors) - 1)]
        self.shapeColor = self.colors[randint(0, len(self.colors) - 1)]
        self.innerShapeColor = self.colors[randint(0, len(self.colors) - 1)]
        self.colorShapeText = self.colors[randint(0, len(self.colors) - 1)]
        self.numberColor = self.colors[randint(0, len(self.colors) - 1)]
        self.backgroundColor = self.colors[randint(0, len(self.colors) - 1)]
        self.colorColorText = self.colors[randint(0, len(self.colors) - 1)]
        # Pick correct text border
        self.shapeBorder = self.borderColors[self.shapeColor]
        self.innerShapeBorder = self.borderColors[self.innerShapeColor]
        self.shapeTextBorder = self.borderColors[self.colorShapeText]
        self.colorTextBorder = self.borderColors[self.colorColorText]
        self.numberBorder = self.borderColors[self.numberColor]
        # Render texts and texts borders
        self.shapeTextRender = renderTextWithBorder(self.shapeText, self.textFont, self.colorShapeText,
                                                    self.shapeTextBorder, 3)
        self.colorTextRender = renderTextWithBorder(self.colorText, self.textFont, self.colorColorText,
                                                    self.colorTextBorder, 3)
        self.fakeNumberRender = renderTextWithBorder(str(self.fakeNumber), self.fakeNumberFont, self.numberColor,
                                                     self.numberBorder, 2)

    def __str__(self):
        return f"Box in Position {self.position}\nNumber: {self.number}\nFake number: {self.fakeNumber}\n" \
               f"Shape: {self.shape}\nInner shape: {self.innerShape}\nShape text: {self.shapeText}\n" \
               f"Color text: {self.colorText}\nShape color: {self.shapeColor}\n" \
               f"Inner shape color: {self.innerShapeColor}\nColor shape text: {self.colorShapeText}\n" \
               f"Number color: {self.numberColor}\nBackground color: {self.backgroundColor}\n" \
               f"Color color text: {self.colorColorText}\nBorder color: {self.shapeBorder}\n"

    def draw(self, gamephase, countvalueframes=None, countvalue=None):
        if gamephase == "phase1":
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect)
            if countvalue == 1:
                self.screen.blit(self.numberRender, (self._x + 70, self._y + 45))
            else:
                self.font = pygame.font.Font('freesansbold.ttf', countvalueframes * 3)
                self.numberRender = self.font.render(str(self.number), True, (255, 255, 255))
                self.screen.blit(self.numberRender,
                                 (self._x + 130 - countvalueframes, self._y + 105 - countvalueframes))
        elif gamephase == "phase2":
            pygame.draw.rect(self.screen, self.backgroundColor, self.rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 5)
            match self.shape:
                case "rectangle":
                    pygame.draw.rect(self.screen, self.shapeBorder, (self._x + 22, self._y + 47, 206, 156), 5)
                    pygame.draw.rect(self.screen, self.shapeColor, (self._x + 25, self._y + 50, 200, 150))
                case "square":
                    pygame.draw.rect(self.screen, self.shapeBorder, (self._x + 22, self._y + 22, 206, 206), 5)
                    pygame.draw.rect(self.screen, self.shapeColor, (self._x + 25, self._y + 25, 200, 200))
                case "circle":
                    pygame.draw.circle(self.screen, self.shapeBorder, (self._x + 125, self._y + 125), 103, 5)
                    pygame.draw.circle(self.screen, self.shapeColor, (self._x + 125, self._y + 125), 100)
                case "triangle":
                    pygame.draw.polygon(self.screen, self.shapeColor, (
                        (self._x + 25, self._y + 212), (self._x + 125, self._y + 39), (self._x + 225, self._y + 212)))
                    pygame.draw.polygon(self.screen, self.shapeBorder, (
                        (self._x + 25, self._y + 212), (self._x + 125, self._y + 39), (self._x + 225, self._y + 212)),
                                        5)
                case _:
                    print("self.shape wrong value")
            match self.innerShape:
                case "rectangle":
                    pygame.draw.rect(self.screen, self.innerShapeBorder, (self._x + 75, self._y + 100, 100, 51))
                    pygame.draw.rect(self.screen, self.innerShapeColor, (self._x + 78, self._y + 103, 94, 46))
                case "square":
                    pygame.draw.rect(self.screen, self.innerShapeBorder, (self._x + 100, self._y + 100, 52, 52))
                    pygame.draw.rect(self.screen, self.innerShapeColor, (self._x + 103, self._y + 103, 46, 46))
                case "circle":
                    pygame.draw.circle(self.screen, self.innerShapeBorder, (self._x + 125, self._y + 125), 25)
                    pygame.draw.circle(self.screen, self.innerShapeColor, (self._x + 125, self._y + 125), 23)
                case "triangle":
                    pygame.draw.polygon(self.screen, self.innerShapeBorder, (
                        (self._x + 93, self._y + 150), (self._x + 158, self._y + 150), (self._x + 125, self._y + 98)))
                    pygame.draw.polygon(self.screen, self.innerShapeColor, (
                        (self._x + 98, self._y + 147), (self._x + 152, self._y + 147), (self._x + 125, self._y + 103)))
                case _:
                    print("self.innerShape wrong value")
            self.screen.blit(self.colorTextRender, (self._x + 125 - self.colorTextRender.get_width() / 2, self._y + 48))
            self.screen.blit(self.shapeTextRender,
                             (self._x + 125 - self.shapeTextRender.get_width() / 2, self._y + 158))
            self.screen.blit(self.fakeNumberRender,
                             (self._x + 125 - self.fakeNumberRender.get_width() / 2, self._y + 103))

    def __getitem__(self, item):
        match item:
            # ints
            case 0:
                return "shape"
            case 1:
                return "inner shape"
            case 2:
                return "shape text"
            case 3:
                return "color text"
            case 4:
                return "shape color"
            case 5:
                return "inner shape color"
            case 6:
                return "color shape text"
            case 7:
                return "number color"
            case 8:
                return "number color"
            case 9:
                return "color color text"
            # Strings
            case "realNumber":
                return self.number
            case "shape":
                return self.shape
            case "inner shape":
                return self.innerShape
            case "shape text":
                return self.shapeText
            case "color text":
                return self.colorText
            case "shape color":
                return self.shapeColor
            case "inner shape color":
                return self.innerShapeColor
            case "color shape text":
                return self.colorShapeText
            case "number color":
                return self.numberColor
            case "number color":
                return self.backgroundColor
            case "color color text":
                return self.colorColorText
            case _:
                return "index out of range"
