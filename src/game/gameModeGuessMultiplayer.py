import itertools
import random
import time
import requests
import json

from src.game.gameModeAbstract import gameModeAbstract
from src.leaderboard.leaderboardImpl import leaderboardImpl
from src.view.viewImpl import viewImpl


class gameModeGuessMultiplayer(gameModeAbstract):
    data = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://htwberlin.com/ssr/superhirnserver/move_schema.json",
        "title": "Move",
        "gameid": 0,
        "gamerid": "",
        "positions": 0,
        "colors": 0,
        "value": ""
    }
    headers = {
        'Content-Type': 'application/json'
    }

    def __init__(self, colors: list, maxTries: int, codeLength: int, autoGuess: str, name: str, ipaddress: str,
                 port: str) -> None:
        self.view: viewImpl = viewImpl()
        self.selfGuess = autoGuess
        self.name = name
        self.colors: list = colors
        self.maxTries: int = maxTries
        self.codeLength: int = codeLength
        self.allSolutions: set = set(itertools.product(colors, repeat=codeLength))
        self.codePool = list(self.allSolutions.copy())
        random.shuffle(self.codePool)
        self.code = self.codePool[0]
        self.leaderboard = None  # initialization of leaderboard
        if ipaddress == "":
            self.ipaddress = "127.0.0.1"
        else:
            self.ipaddress = ipaddress
        if port == "":
            self.port = 8000
        else:
            self.port = port

        # single initialization of leaderboard to keep it for the entire game
        if self.leaderboard is None:
            self.leaderboard = leaderboardImpl()

    def gameLoop(self, startTime: float):
        self.makeStartGameRequest()
        named_tuple = time.localtime()  # get struct_time
        time_string = time.strftime("%H:%M:%S", named_tuple)
        guesses: list = []
        listCorrectPositions: list = []
        listCorrectColors: list = []
        tries: int = 0
        gameIsWon: bool = False
        while tries < self.maxTries:
            if self.selfGuess == "n":
                inputList: tuple = self.makePseudoRandomGuess()
                guesses.append(inputList)
                time.sleep(1)
            else:
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
                        codeList: tuple = tuple([int(x) for x in code])
                        for elem in codeList:
                            if not elem in self.colors:
                                self.view.printToTerminal(
                                    "Der Code enthält Farben die nicht in der momentanten Farbauswahl enthalten sind, bitte gib einen anderen Code ein")
                                break
                        else:
                            guesses.append(codeList)
                            break

            # Make feedback Request
            feedback = self.makeFeedbackRequest(guesses[-1])

            listCorrectPositions.append(feedback[0])
            listCorrectColors.append(feedback[1])

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
            if feedback[0] == self.codeLength:
                gameIsWon = True
                break
            self.removeImpossibleGuesses(guesses[-1], feedback[0], feedback[1])

            tries += 1
        elapsedTime = time.time() - startTime
        if gameIsWon == True:
            self.view.printToTerminal(self.printResult(True, elapsedTime, tries))
        else:
            self.view.printToTerminal(self.printResult(False, elapsedTime, tries))

    def represents_int(self, s) -> bool:
        try:
            int(s)
        except ValueError:
            return False
        else:
            return True

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

    def makeFeedbackRequest(self, guess) -> tuple:
        self.data["value"] = self.convertTuple(guess)

        dest = "http://" + self.ipaddress + ":" + str(self.port)
        print(self.data)
        # send post-request with requests.post()
        try:
            response = requests.post(dest, json.dumps(self.data), self.headers)
            print(response)

            # check response status code
            if response.status_code == 200:
                r = response.json()
                feedback = r["value"]
                print("Here" + feedback)
                correctPositions = feedback.count("8")
                correctColors = feedback.count("7")
                return (correctPositions, correctColors)

            else:
                print("POST request failed with status code:", response.status_code)
                print("Server konnte nicht ereicht werden... Programm wird geschlossen")
                exit()

        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)
            print("Server konnte nicht ereicht werden... Programm wird geschlossen")
            exit()

    def makeStartGameRequest(self):
        self.data["gamerid"] = self.name
        self.data["positions"] = self.codeLength
        self.data["colors"] = len(self.colors)
        self.data["gameid"] = 0
        dest = "http://" + self.ipaddress + ":" + str(self.port)
        # send post-request with requests.post()
        try:
            response = requests.post(dest, json.dumps(self.data), self.headers)

            # check response status code
            if response.status_code == 200:
                r = response.json()
                self.data["gameid"] = r["gameid"]

            else:
                print("POST request failed with status code:", response.status_code)

        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    def convertTuple(self, tup):
        tupleStr = ''
        for item in tup:
            tupleStr = tupleStr + str(item)
        return tupleStr
