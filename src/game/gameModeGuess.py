import itertools
import random
import time


from src.game.gameModeAbstract import gameModeAbstract
from src.leaderboard.leaderboardImpl import leaderboardImpl
from src.view.viewImpl import viewImpl


class gameModeGuess(gameModeAbstract):

    def __init__(self, colors: list, maxTries: int, codeLength: int) -> None:
        self.view: viewImpl = viewImpl()
        self.colors: list = colors
        self.maxTries: int = maxTries
        self.codeLength: int = codeLength
        self.allSolutions: list = list(itertools.product(colors, repeat=codeLength))
        random.shuffle(self.allSolutions)
        self.code = self.allSolutions[0]
        self.leaderboard = None   # initialization of leaderboard

        # single initialization of leaderboard to keep it for the entire game
        if self.leaderboard is None:
            self.leaderboard = leaderboardImpl()

    def gameLoop(self, startTime) -> None:
        named_tuple = time.localtime()  # get struct_time
        time_string = time.strftime("%H:%M:%S", named_tuple)
        guesses: list = []
        listCorrectPositions: list = []
        listCorrectColors: list = []
        tries: int = 0
        gameIsWon: bool = False
        while tries < self.maxTries:
            codeList: list = []
            while True:

                code: str = self.view.takeInputFromUser(
                    "Bitte gib deinen Versuch ein (Format 12345): "
                )

                if self.represents_int(code) == False:
                    self.view.printToTerminal("Bitte gib eine Nummer ein")
                    continue
                elif not len(code) == self.codeLength:
                    self.view.printToTerminal("Bitte gib eine " + str(self.codeLength) + " stellige Zahl ein")
                    continue
                else:
                    codeList: list = [int(x) for x in code]
                    for elem in codeList:
                        if not elem in self.colors:
                            self.view.printToTerminal(
                                "Der Code enthält Farben die nicht in der momentanten Farbauswahl enthalten sind, bitte gib einen anderen Code ein")
                            break
                    else: break



            guesses.append(codeList)
            correctPositions, correctColor = self.determineCorrectPicks(
                codeList, self.code
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
                    time_string)
            )
            if correctPositions == self.codeLength:
                gameIsWon = True
                break


            tries += 1
        elapsedTime = time.time() - startTime
        if gameIsWon == True:


            self.view.printToTerminal(self.printResult(True, elapsedTime, tries))

            # entry into leaderboard
            while True:
                playerName = self.view.takeInputFromUser("Bitte gib deinen Namen ein: ")
                if playerName == "":
                    playerName = "player"
                if len(playerName) > 10: 
                    self.view.printToTerminal("Bitte gib einen Namen der kürzer ist als 10 Zeichen") 
                    continue
                else:
                    break

            self.updateLeaderboard(playerName, tries, elapsedTime, len(self.colors), self.codeLength)
        else:
            self.view.printToTerminal(self.printResult(False, elapsedTime, tries))

    def updateLeaderboard(self, name: str, numberOfTrys: int, timeElapsed: time, colors: int, codeLength: int) -> None:
        if self.leaderboard is None:
            self.leaderboard = leaderboardImpl()

        self.leaderboard.newLeaderboardEntry(name, numberOfTrys, timeElapsed, colors, codeLength)
        self.leaderboard.saveData()  # added to save the leaderboard

        # Debug print statement to check if the entry was added successfully
        print("Updating Leaderboard...\n", self.leaderboard.showLeaderboard())

    def represents_int(self, s) -> bool:
        try:
            int(s)
        except ValueError:
            return False
        else:
            return True
