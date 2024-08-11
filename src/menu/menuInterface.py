from abc import ABC, abstractmethod

class menuInterface(ABC):
    """Shows the Menu and gives back a string of which menu item was selected
    @return String of the option selected"""
    @abstractmethod
    def showMenu(self) -> str:
        pass
