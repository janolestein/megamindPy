import itertools as itertools
from src.game.gameModeAbstract import gameModeAbstract
from src.view.viewImpl import viewImpl
import random
import time


class gameModeCode(gameModeAbstract):

    def __init__(self, code: int, colors: list, maxTries: int, codeLength: int) -> None:
        self.view: viewImpl = viewImpl()
        self.code: list = [int(x) for x in str(code)]
        self.colors: list = colors
        self.maxTries: int = maxTries
        self.codeLength: int = codeLength

        self.allSolutions: set = set(itertools.product(colors, repeat=codeLength))

    def gameLoop(self, startTime) -> None:
        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%H:%M:%S", named_tuple)
        guesses: list = []
        listCorrectPositions: list = []
        listCorrectColors: list = []
        tries: int = 0
        gameIsWon: bool = False
        while tries < self.maxTries:
            inputList: tuple = self.makePseudoRandomGuess()
            guesses.append(inputList)
            correctPositions, correctColor = self.determineCorrectPicks(
                inputList, self.code
            )
            listCorrectPositions.append(correctPositions)
            listCorrectColors.append(correctColor)

            self.view.printGameBoard(
                self.drawGameBoard(
                    guesses,
                    listCorrectPositions,
                    listCorrectColors,
                    self.codeLength,
                    self.maxTries,
                    tries,
                    time_string                )
            )
            if correctPositions == self.codeLength:
                gameIsWon = True
                break
            self.removeImpossibleGuesses(inputList, correctPositions, correctColor)
            time.sleep(1)

            tries += 1
        elapsedTime = time.time() - startTime
        if gameIsWon == True:
            self.view.printToTerminal(self.printResult(False, elapsedTime, tries))
        else:
            self.view.printToTerminal(self.printResult(True, elapsedTime, tries))

    def makePseudoRandomGuess(self) -> tuple:
        return self.allSolutions.pop()

    def removeImpossibleGuesses(self, guess, correctPositions, correctColor) -> None:
        rand = random.randint(1, 2)
        if rand == 1:
            return
        tempAllSolutions: set = self.allSolutions.copy()
        for elem in tempAllSolutions:
            correctPositionsOfElem, correctColorsOfElem = self.determineCorrectPicks(
                elem, guess
            )
            if (
                correctPositions != correctPositionsOfElem
                or correctColor != correctColorsOfElem
            ):
                self.allSolutions.remove(elem)
