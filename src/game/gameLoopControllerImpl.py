import time

from src.game import gameModeGuessMultiplayer
from src.game.gameLoopControllerInterface import gameLoopControllerInterface
from src.game.gameModeCode import gameModeCode
from src.leaderboard.leaderboardImpl import leaderboardImpl
from src.view.viewImpl import viewImpl
from src.model.modelImpl import modelImpl
from src.game.gameModeGuess import gameModeGuess
from src.game.gameModeGuessMultiplayer import gameModeGuessMultiplayer
from src.game.Server import startServer


class gameLoopControllerImpl(gameLoopControllerInterface):
    availableColors: list
    colorsInUse: list
    maxTries: int
    codeLength: int = 5

    def __init__(self) -> None:
        self.view: viewImpl = viewImpl()
        self.leaderboard: leaderboardImpl = leaderboardImpl()
        self.model: modelImpl = modelImpl()
        self.availableColors, self.maxTries = self.model.getGameData()
        self.availableColors: list = list(map(int, self.availableColors))
        self.colorsInUse = self.availableColors

    def startGameMode(
            self,
            modus: str,
            fromParameters=False,
            codeLengthFromParamters: int = -1,
            colorsFromParameters: int = -1,
    ) -> None:
        if fromParameters:
            self.codeLength = codeLengthFromParamters
            self.colorsInUse = self.availableColors[:colorsFromParameters]
        elif modus == "multiplayerCode":
            self.startGameAsCodeMultiplayer()
        else:
            self.askForCodeLengthAndColors()

        match modus:
            case "code":
                self.startGameAsCode()
            case "guess":
                self.startGameAsGuesser()
            case "multiplayerCode":
                pass
            case "multiplayerGuess":
                self.startGameAsGuesserMultiplayer()
            case _:
                print("something went wrong starting the game")

    def startGameAsCode(self) -> None:
        while True:

            code: str = self.view.takeInputFromUser(
                "Bitte gib den Code ein, den das Program erraten soll: "
            )
            if self.represents_int(code) == False:
                self.view.printToTerminal("Bitte gib eine Nummer ein")
                continue
            elif not len(code) == self.codeLength:
                self.view.printToTerminal(
                    "Bitte gib eine " + str(self.codeLength) + " stellige Zahl ein"
                )
                continue
            else:
                codeList: list = [int(x) for x in code]
                for elem in codeList:
                    if not elem in self.colorsInUse:
                        self.view.printToTerminal(
                            "Der Code enthält Farben die nicht in der momentanten Farbauswahl enthalten sind, bitte gib einen anderen Code ein"
                        )
                        break
                else:
                    break

        modeCode: gameModeCode = gameModeCode(
            int(code), self.colorsInUse, self.maxTries, self.codeLength
        )
        modeCode.startGameMode(time.time())

    def startGameAsGuesser(self):
        modeGuesser: gameModeGuess = gameModeGuess(
            self.colorsInUse, self.maxTries, self.codeLength
        )
        modeGuesser.startGameMode(time.time())

    def startGameAsCodeMultiplayer(self) -> None:
        ipaddress = self.view.takeInputFromUser(
            "Bitte gib eine IP Adresse ein (leer für Localhost): "
        )
        port = self.view.takeInputFromUser(
            "Bitte gib einen Port ein (leer für 8000): "
        )
        while True:
            input = self.view.takeInputFromUser("code selbst erstellen? (y/n)")
            if input == "y" or input == "n":
                startServer(self.availableColors, input, ipaddress, port)
                break

    def startGameAsGuesserMultiplayer(self):
        ipaddress = self.view.takeInputFromUser(
            "Bitte gib eine IP Adresse ein (leer für Localhost): "
        )
        port = self.view.takeInputFromUser(
            "Bitte gib einen Port ein (leer für 8000): "
        )

        name = self.view.takeInputFromUser("Bitte gib einen Spielernamen ein: ")
        while True:
            autoGuess = self.view.takeInputFromUser("möchstest du selbst raten (y/n): ")
            if not (autoGuess == "y" or autoGuess == "n"):
                self.view.printToTerminal("Bitte gib y oder n ein")
                continue
            else:
                break

        modeGuesserMultiplayer: gameModeGuessMultiplayer = gameModeGuessMultiplayer(
            self.colorsInUse, self.maxTries, self.codeLength, autoGuess, name, ipaddress, port
        )
        modeGuesserMultiplayer.startGameMode(time.time())


    def askForCodeLengthAndColors(self) -> None:
        while True:
            pickedColors: str = self.view.takeInputFromUser(
                "Mit wie vielen Farben möchstest du spielen? Min=2, Max=8 leer lassen für standard: ("
                + str(len(self.colorsInUse))
                + ")"
            )
            if pickedColors == "":
                break
            elif self.represents_int(pickedColors) == False:
                self.view.printToTerminal("Bitte gib eine Zahl ein")
                continue
            elif 2 <= int(pickedColors) <= 8:
                self.colorsInUse = self.availableColors[: int(pickedColors)]
                break
            else:
                self.view.printToTerminal("Bitte gib eine Zahl zwischen 2 und 8 ein")

        while True:
            pickedCodeLength: str = self.view.takeInputFromUser(
                "Wie lang soll der Code sein, der geraten werden soll. 4 oder 5 Stellen. Leer lassen für Standard: ("
                + str(self.codeLength)
                + ")"
            )
            if pickedCodeLength == "":
                break
            elif self.represents_int(pickedCodeLength) == False:
                self.view.printToTerminal("Bitte gib eine Zahl ein")
                continue
            elif 4 <= int(pickedCodeLength) <= 5:
                self.codeLength = int(pickedCodeLength)
                break
            else:
                self.view.printToTerminal("Bitte gib eine Zahl zwischen 2 und 8 ein")

    def represents_int(self, s) -> bool:
        try:
            int(s)
        except ValueError:
            return False
        else:
            return True
