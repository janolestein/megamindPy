import json
from os import linesep

from src.leaderboard.leaderboardInterface import leaderboardInterface
from datetime import time


class leaderboardImpl(leaderboardInterface):

    def __init__(self):
        self.leaderboard = []
        self.loadJson()


    def loadJson(self) -> None:
        try:
            with open('leaderboard.json') as f:
                self.leaderboard = json.load(f)
        except FileNotFoundError:
            pass


    def showLeaderboard(self) -> str:
        self.loadJson()
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: (x['numberOfTrys'], x['timeElapsed']))
        leaderboard_str = "Leaderboard:\n"
        leaderboard_str += "-" * 40 + linesep
        for i, entry in enumerate(sorted_leaderboard, start=1):
            minutes = int(entry['timeElapsed'] / 60)
            seconds = round(round(entry['timeElapsed']) - minutes * 60)
            leaderboard_str += f"{i}. Name: {entry['name']}, Versuche: {entry['numberOfTrys']}, Zeit: {minutes}:{seconds}, Farbanzahl: {entry['colors']}, Codelaenge: {entry['codeLength']}\n"
            leaderboard_str += "-"*40 + linesep
        return leaderboard_str


    def newLeaderboardEntry(self, name: str, numberOfTrys: int, timeElapsed: time, colors: int, codeLength: int) -> None:
        entry = {"name": name, "numberOfTrys": numberOfTrys, "timeElapsed": timeElapsed, "colors": colors, "codeLength": codeLength}
        self.leaderboard.append(entry)

        # Print the leaderboard contents after adding a new entry
        # print("Result:", self.leaderboard)

    def saveData(self) -> None:
        with open('leaderboard.json', 'w') as f:
            json.dump(self.leaderboard, f)

