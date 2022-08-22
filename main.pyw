import pygame
from random import shuffle, randint
import box
import textbox
import button
import timebar
import json


def numberGenerator():
    numbers = [1, 2, 3, 4]
    shuffle(numbers)
    for i in range(4):
        yield numbers.pop(0)


class Game:
    gameWon: bool
    gameWins: int
    gamePhase: str
    countValue: int
    countValueFrames: int
    numberBoxes: [box.Box, box.Box, box.Box, box.Box]
    askedObjects: ((int, str), (int, str))
    question: str
    questionRender: pygame.surface.Surface
    expectedAnswer: str
    expectedAnswerRender: pygame.surface.Surface

    def __init__(self):
        # First
        pygame.init()
        with open("config.json") as file:
            self.config = json.load(file)
            # print(self.config)
        self.screen = pygame.display.set_mode((1275, 760))
        # order doesn't care
        self.fps = self.config["fps"]
        self.running = True
        self.startBtn = button.Button(self.screen, (485, 300), (300, 160), 72, "START",
                                      self.config["color"]["startButton"]["normal"],
                                      self.config["color"]["startButton"]["hover"],
                                      self.config["color"]["startButton"]["pressed"])
        self.playAgainBTn = button.Button(self.screen, (385, 300), (500, 160), 72, "PLAY AGAIN",
                                          self.config["color"]["startButton"]["normal"],
                                          self.config["color"]["startButton"]["hover"],
                                          self.config["color"]["startButton"]["pressed"])
        self.textBox = textbox.TextBox(self.screen, 387, 550, 500, 70)
        self.font72 = pygame.font.Font('freesansbold.ttf', 72)
        self.font24 = pygame.font.Font('freesansbold.ttf', 24)
        self.font12 = pygame.font.Font('freesansbold.ttf', 12)
        self.numberRenders = {1: self.font72.render("1", True, (255, 255, 255)),
                              2: self.font72.render("2", True, (255, 255, 255)),
                              3: self.font72.render("3", True, (255, 255, 255)),
                              4: self.font72.render("4", True, (255, 255, 255))}
        pygame.display.set_caption("BANK HACKING GAME")
        self.timeBar = timebar.TimeBar(self.screen, 50, 400, 26, 1176, self.config["roundTime"])
        self.winRender = self.font72.render("WIN!!!", True, (255, 255, 255))
        self.loseRender = self.font72.render("LOSE!!!", True, (255, 255, 255))
        # Last
        self.gameReset()
        self.clock = pygame.time.Clock()
        self.game_loop()

    def roundReset(self):
        self.textBox.reset()
        self.timeBar.reset()
        self.gamePhase = "phase1"
        self.countValueFrames = 60
        self.countValue = 1
        realNumberGenerator = numberGenerator()
        fakeNumberGenerator = numberGenerator()
        self.numberBoxes = [
            box.Box(self.screen, next(realNumberGenerator), 0, next(fakeNumberGenerator), self.config["color"]["box"],
                    self.config["shapes"]),
            box.Box(self.screen, next(realNumberGenerator), 1, next(fakeNumberGenerator), self.config["color"]["box"],
                    self.config["shapes"]),
            box.Box(self.screen, next(realNumberGenerator), 2, next(fakeNumberGenerator), self.config["color"]["box"],
                    self.config["shapes"]),
            box.Box(self.screen, next(realNumberGenerator), 3, next(fakeNumberGenerator), self.config["color"]["box"],
                    self.config["shapes"])]
        firstNum, secondNum = randint(0, 3), randint(0, 3)
        self.askedObjects = ((firstNum, self.numberBoxes[firstNum][randint(0, 9)]),
                             (secondNum, self.numberBoxes[secondNum][randint(0, 9)]))
        self.question = f"{self.askedObjects[0][1]} ({self.numberBoxes[self.askedObjects[0][0]].number}) and" \
                        f" {self.askedObjects[1][1]} ({self.numberBoxes[self.askedObjects[1][0]].number})"

        self.questionRender = self.font24.render(self.question, True, "white")
        self.expectedAnswer = f"{self.numberBoxes[self.askedObjects[0][0]][self.askedObjects[0][1]]} " \
                              f"{self.numberBoxes[self.askedObjects[1][0]][self.askedObjects[1][1]]}"
        # print(self.numberBoxes[0].number, self.numberBoxes[1].number, self.numberBoxes[2].number,
        #    self.numberBoxes[3].number)
        # print(f"QUESTION: {self.question}\nEXPECTED ANSWER: {self.expectedAnswer}")
        self.winRender = self.font72.render("WIN!!!", True, (255, 255, 255))
        self.loseRender = self.font72.render("LOSE!!!", True, (255, 255, 255))
        self.expectedAnswerRender = self.font12.render(f"Expected answer: '{self.expectedAnswer}'", True,
                                                       (255, 255, 255))

    def gameReset(self):
        self.gameWon = False
        self.gameWins = 0
        self.roundReset()
        self.gamePhase = "start"
        self.countValue = 3


    def graphic(self):
        self.screen.fill(self.config["color"]["bgColor"])
        if self.gamePhase == "start":
            self.startBtn.draw(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        elif self.gamePhase == "counting down":
            self.screen.blit(self.numberRenders[self.countValue], (650, 300))
        elif self.gamePhase == "phase1":
            for i in self.numberBoxes:
                i.draw("phase1", self.countValueFrames, self.countValue)
        elif self.gamePhase == "phase2":
            self.textBox.draw(pygame.time.get_ticks())
            for i in self.numberBoxes:
                i.draw("phase2")
            self.timeBar.draw()
            self.screen.blit(self.questionRender, (638 - self.questionRender.get_width() / 2, 450))
        elif self.gamePhase == "endScreen":
            if self.gameWon:
                self.screen.blit(self.winRender, (638 - self.winRender.get_width() / 2, 150))
            elif not self.gameWon:
                self.screen.blit(self.loseRender, (638 - self.loseRender.get_width() / 2, 150))
            self.playAgainBTn.draw(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
            self.screen.blit(self.expectedAnswerRender, (638 - self.expectedAnswerRender.get_width() / 2, 700))

        pygame.display.update()

    def countDown(self):
        self.countValueFrames -= 1
        if self.countValueFrames == 0:
            self.countValue -= 1
            self.countValueFrames = 60
        if self.countValue == 0:
            if self.gamePhase == "counting down":
                self.gamePhase = "phase1"
                self.countValueFrames = 60
                self.countValue = 1
            elif self.gamePhase == "phase1" and self.countValueFrames == 1:
                self.gamePhase = "phase2"
                self.textBox.active = True

    def logic(self):
        if self.gamePhase == "start":
            if self.startBtn.isClicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0]):
                self.gamePhase = "counting down"
        elif self.gamePhase == "counting down" or self.gamePhase == "phase1":
            self.countDown()
        elif self.gamePhase == "phase2":
            if self.timeBar.end():
                self.gamePhase = "endScreen"
                if self.textBox.text == self.expectedAnswer:
                    print("jesteś zajebisty")
                    if self.gameWins < 2:
                        self.gameWins += 1
                        self.roundReset()
                    else:
                        self.gameWon = True
                        self.gamePhase = "endScreen"
                else:
                    print("debil")
                    self.gameWon = False
        elif self.gamePhase == "endScreen":
            if self.playAgainBTn.isClicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0]):
                self.gameReset()

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.textBox.service(event) == "enter":
                        if self.textBox.text == self.expectedAnswer:
                            print("kox")
                            if self.gameWins < 2:
                                self.gameWins += 1
                                self.roundReset()
                            else:
                                self.gameWon = True
                                self.gamePhase = "endScreen"
                        else:
                            print("debil")
                            self.gameWon = False
                            self.gamePhase = "endScreen"
            self.logic()
            self.graphic()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Game()
    pygame.quit()
