from abc import ABC, abstractmethod


class modelInterface(ABC):
    """Reads in the File with the Leaderboard Data and returns it
    @return Leaderboard as a string"""

    @abstractmethod
    def getLeaderboardData(self) -> str:
        pass

    """Returns the colors available
    @return Colors as a Enum"""

    @abstractmethod
    def getGameData(self) -> tuple:
        pass

    """Saves a new Version of the Leaderboard to the file"""

    @abstractmethod
    def saveData(self) -> None:
        pass
