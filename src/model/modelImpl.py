import json
from enum import IntEnum

from src.model.modelInterface import modelInterface


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance
class colors(IntEnum):
    ROT = 1
    GRUEN = 2
    GELB = 3
    BLAU = 4
    ORANGE = 5
    BRAUN = 6
    WEISS = 7
    SCHWARZ = 8

class modelImpl(modelInterface, SingletonClass):
    maxTries = 10

    def __init__(self):
        self.leaderboard = None

    def getLeaderboardData(self) -> str:
        #return super().getLeaderboardData()
        return "leaderboard_data.json"
    def saveLeaderboardData(self, leaderboard_data):
        with open("leaderboard_data.json", "w") as file:
            json.dump(leaderboard_data, file)

    def loadLeaderboardData(self):
        try:
            with open("leaderboard_data.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []



    
    def getGameData(self) -> tuple:
        return colors, self.maxTries 

    def saveData(self) -> None:
        return super().saveData()
