from src.view.viewInterface import viewInterface
import os as os

class viewImpl(viewInterface):
    def printToTerminal(self, toDisplay: str) -> None:
        print(toDisplay)
        print("")

    def printGameBoard(self, gameBoard: str) -> None:
        os.system("clear")
        print("Legende: # = Noch nicht getätigter Rateversuch, + = Korrekte Position und Farbe, * = Korrekte Farbe, - = Nichts Korrekt" + os.linesep + "Farbkodierung: 1=Rot, 2=Grün, 3=Gelb, 4=Blau, 5=Orange, 6=Braun, 7=Weiss, 8=Schwarz")
        print(gameBoard)

    def takeInputFromUser(self, inputMassage: str) -> str:
        takenInput = input(inputMassage + os.linesep)
        if takenInput == "q":
            print("Vielen Dank fürs spielen" + os.linesep)
            exit()
        return takenInput
