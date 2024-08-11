from abc import ABC, abstractmethod
import time
from os import linesep


class gameModeAbstract(ABC):

    @abstractmethod
    def gameLoop(self, startTime) -> None:
        pass

    def startGameMode(self, startTime) -> None:
        self.gameLoop(startTime)

    def determineCorrectPicks(self, actualPick, pickToCheckAgainst) -> tuple:
        correctPositions: int = 0
        correctColor: int = 0
        incorectGuesses: list = []
        incorecctAnswers: list = []

        for guess, answer in zip(actualPick, pickToCheckAgainst):
            if guess == answer:
                correctPositions += 1
            else:
                incorectGuesses.append(guess)
                incorecctAnswers.append(answer)

        for elem in incorectGuesses:
            if elem in incorecctAnswers:
                incorecctAnswers.remove(elem)
                correctColor += 1

        return correctPositions, correctColor

    def printResult(self, playerHasWon: bool, elapsedTime: float, tries: int) -> str:
        named_tuple = time.localtime() # get struct_time
        endTime = time.strftime("%H:%M:%S", named_tuple)
        minutes = int(elapsedTime / 60)
        seconds = round(round(elapsedTime) - minutes * 60)
        result: str = ""
        result += "-" * 41 + linesep
        if playerHasWon:
            result += "     Du hast gewonnen!" + linesep
        else:
            result += "     Du hast verloren..." + linesep
        result += "-" * 41 + linesep
        result += (
            "Spielende: "
            + endTime
            + linesep
            + "Spiellänge: "
            + str(minutes)
            + " Minuten "
            + str(seconds)
            + " Sekunden"
            + linesep
            + "Rateversuche: "
            + str(tries)
            + linesep
        )
        result += "-" * 41 + linesep
        return result

    def drawGameBoard(
        self,
        picks: list,
        feedbackPositions: list,
        feedbackColors: list,
        codeLength: int,
        maxTries: int,
        currentNumberOfTries: int,
        startTime: str,
    ) -> str:
        gameBoard: str = "Spielbegin: " + startTime + linesep
        for index in range(maxTries):
            if index <= currentNumberOfTries:
                if index == 9:
                    gameBoard += (
                        f"Versuch {index + 1}: {picks[index]}"
                        + linesep
                        + "Feedback:    "
                        + "+  " * feedbackPositions[index]
                        + "*  " * feedbackColors[index]
                        + linesep
                    )
                else:
                    gameBoard += (
                        f"Versuch {index + 1}: {picks[index]}"
                        + linesep
                        + "Feedback:   "
                        + "+  " * feedbackPositions[index]
                        + "*  " * feedbackColors[index]
                        + linesep
                    )
                gameBoard += "-" * 30 + linesep
            else:
                if index == 9:
                    gameBoard += (
                        f"Versuch {index + 1}: "
                        + "#  " * codeLength
                        + linesep
                        + "Feedback:   "
                        + "-  " * codeLength
                        + linesep
                    )
                else:
                    gameBoard += (
                        f"Versuch {index + 1}: "
                        + "#  " * codeLength
                        + linesep
                        + "Feedback:  "
                        + "-  " * codeLength
                        + linesep
                    )
                gameBoard += "-" * 30 + linesep

        return gameBoard
