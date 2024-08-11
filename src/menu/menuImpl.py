from src.menu.menuInterface import menuInterface
from src.view.viewImpl import viewImpl
from os import linesep


class menuImpl(menuInterface):
    def __init__(self) -> None:
        self.view: viewImpl = viewImpl()

    def showMenu(self) -> str:
        self.view.printToTerminal(
            "_" * 57
            + linesep
            + "Willkommen bei Super-Superhirn!                          |"
            + linesep
            + "-" * 57 + "|"
            + linesep
            + "Bitte wähle aus was du tun möchtest                      |"
            + linesep
            + "deine Optionen sind:                                     |"
            + linesep
            + '"t" um das Tutorial zu öffnen                            |'
            + linesep
            + '"l" um das Leaderboard zu anzuzeigen                     |'
            + linesep
            + '"r" um das Spiel als Rater zu starten                    |'
            + linesep
            + '"k" um das Spiel als Kodierer zu starten                 |'
            + linesep
            + '"mr" um das Spiel als Rater im Multiplayer zu starten    |'
            + linesep
            + '"mk" um das Spiel als Kodierer im Multiplayer zu starten |'
            + linesep
            + '"q" um das Spiel zu beenden                              |'
            + linesep
            + "_" * 57 + "|"
        )
        return self.parseInput()

    def parseInput(self) -> str:
        while True:
            inputMenu: str = self.view.takeInputFromUser("Bitte gib deine Auswahl ein:")

            match inputMenu:
                case "t":
                    return "t"
                case "l":
                    return "l"
                case "r":
                    return "r"
                case "k":
                    return "k"
                case "mr":
                    return "mr"
                case "mk":
                    return "mk"
                case _:
                    self.view.printToTerminal(
                        "Bitte wähle eine der vorgebenen Optionen aus" + linesep
                    )
