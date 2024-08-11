from abc import ABC, abstractmethod

class gameLoopControllerInterface(ABC):
    """Starts a new Game with specified mode
    @param game Modus to start as a string"""
    @abstractmethod
    def startGameMode(self, modus: str) -> None:
        pass
