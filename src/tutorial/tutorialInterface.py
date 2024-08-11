from abc import ABC, abstractmethod


class tutorialInterface(ABC):
    """Returns a String to be displayed as the tutorial
    @return Tutorial as a String"""

    @abstractmethod
    def showTutorial(self) -> str:
        pass
