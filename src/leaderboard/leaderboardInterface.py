from abc import ABC, abstractmethod
from datetime import time


class leaderboardInterface(ABC):
    """Returns the current Leaderboard as String to be displayd 
    @return leaderboard as a String"""

    @abstractmethod
    def showLeaderboard(self) -> str:
        pass

    """Makes a new entry into the Leaderboard
    @param name of the player as a String
    @param number of trys needed to win the game as an int
    @param amount of time used to win the game as time from the datetime module"""

    @abstractmethod
    def newLeaderboardEntry(self, name: str, numberOfTrys: int, timeElapsed: time) -> None:
        pass
