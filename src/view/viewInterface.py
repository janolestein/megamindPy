from abc import ABC, abstractmethod

class viewInterface(ABC):
    """Method to print a string to the terminal to by displayed """
    @abstractmethod
    def printToTerminal(self, toDisplay: str):
        pass

    @abstractmethod
    def printGameBoard(self, gameBoard: str):
        pass

    @abstractmethod
    def takeInputFromUser(self, inputMassage: str) -> str:
        pass
