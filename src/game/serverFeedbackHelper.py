import itertools as itertools
from src.game.gameModeAbstract import gameModeAbstract
from src.view.viewImpl import viewImpl
import random



class serverFeedbackHelper(gameModeAbstract):

    def __init__(self, numColorsToUse: int, colors: list, codeLength: int, autoCode: bool, code) -> None:
        self.view: viewImpl = viewImpl()
        self.colors: list = colors[:numColorsToUse]
        self.codeLength: int = codeLength
        if autoCode:
            self.allSolutions: list = list(itertools.product(self.colors, repeat=self.codeLength))
            random.shuffle(self.allSolutions)
            self.code = self.allSolutions[0]
        else:
            self.code = code

    def giveFeedback(self, pick: int) -> tuple:
        return self.determineCorrectPicks(pick, self.code)

    def getCode(self) -> list:
        return self.code

    # This is not used
    def gameLoop(self, startTime) -> None:
        return super().gameLoop(startTime)
