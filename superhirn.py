import argparse
from src.leaderboard.leaderboardImpl import leaderboardImpl
from src.menu.menuImpl import menuImpl
from src.tutorial.tutorialImpl import tutorialImpl
from src.view.viewImpl import viewImpl
from os import linesep

from src.game.gameLoopControllerImpl import gameLoopControllerImpl

gameLoopController: gameLoopControllerImpl
leaderboard: leaderboardImpl
menu: menuImpl
tutorial: tutorialImpl
view: viewImpl


def main():
    parser = argparse.ArgumentParser(
        prog="Super-Superhirn",
        description="Super-Superhirn als Terminal-Anwendung zum spielen",
        epilog="Starte das Spiel mit Argumenten um direkt in einen Modus zu kommen oder ohne um das Spiel normal zu starten",
    )
    # parser.add_argument("modus", type=str, nargs=1, choices=["-t", "-m", "-l", "-k", "-r"], help="-t = Leaderboard, -m = Menü, -l = Leaderbaord, -k = Als Kodierer spielen, -r = Als Rater spielen")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", action="store_true", help="Öffne das Tutorial")
    group.add_argument("-m", action="store_true", help="Öffne das Menü")
    group.add_argument("-l", action="store_true", help="Öffne das Leaderboard")
    group.add_argument("-k", action="store_true", help="Starte das Spiel als Kodierer")
    group.add_argument("-r", action="store_true", help="Starte das Spiel als Rater")
    group.add_argument("-mk", action="store_true", help="Starte das Spiel als Kodierer im Multiplayer")
    group.add_argument("-mr", action="store_true", help="Starte das Spiel als Rater im Multiplayer")
    group.add_argument("-mkp", nargs=2, type=int, help="Starte den Kodierer Modus mit vorgegebenen Parametern für Kodelänge und Farbanzahl im Multiplayer" + linesep + "1 = Kodelänge(4-5), 2 = Farbanzahl(2-8)")
    group.add_argument("-mrp", nargs=2, type=int, help="Starte den Rater Modus mit vorgegebenen Parametern für Kodelänge und Farbanzahl im Multiplayer")
    group.add_argument("-kp", nargs=2, type=int, help="Starte den Kodierer Modus mit vorgegebenen Parametern für Kodelänge und Farbanzahl" + linesep + "1 = Kodelänge(4-5), 2 = Farbanzahl(2-8)")
    group.add_argument("-rp", nargs=2, type=int, help="Starte den Rater Modus mit vorgegebenen Parametern für Kodelänge und Farbanzahl" + linesep + "1 = Kodelänge(4-5), 2 = Farbanzahl(2-8)")
    args = parser.parse_args()

    if args.kp is not None:
        if not 4 <= args.kp[0] <= 5:
            view.printToTerminal("Codelänge muss zwischen 4 und 5 sein")
            exit()
        elif not 2 <= args.kp[1] <= 8:
            view.printToTerminal("Farbanzahl muss zwischen 2 und 8 sein")
            exit()
        gameLoopController.startGameMode("code", fromParameters=True, codeLengthFromParamters=args.kp[0], colorsFromParameters=args.kp[1])
    elif args.rp is not None:
        if not 4 <= args.kp[0] <= 5:
            view.printToTerminal("Codelänge muss zwischen 4 und 5 sein")
            exit()
        elif not 2 <= args.kp[1] <= 8:
            view.printToTerminal("Farbanzahl muss zwischen 2 und 8 sein")
            exit()
        gameLoopController.startGameMode("guess", fromParameters=True, codeLengthFromParamters=args.rp[0], colorsFromParameters=args.rp[1])
    elif args.mkp is not None:
        if not 4 <= args.mkp[0] <= 5:
            view.printToTerminal("Codelänge muss zwischen 4 und 5 sein")
            exit()
        elif not 2 <= args.mkp[1] <= 8:
            view.printToTerminal("Farbanzahl muss zwischen 2 und 8 sein")
            exit()
        gameLoopController.startGameMode("multiplayerCode", fromParameters=True, codeLengthFromParamters=args.mkp[0], colorsFromParameters=args.mkp[1])
    elif args.mrp is not None:
        if not 4 <= args.mrp[0] <= 5:
            view.printToTerminal("Codelänge muss zwischen 4 und 5 sein")
            exit()
        elif not 2 <= args.mrp[1] <= 8:
            view.printToTerminal("Farbanzahl muss zwischen 2 und 8 sein")
            exit()
        gameLoopController.startGameMode("multiplayerGuess", fromParameters=True, codeLengthFromParamters=args.mrp[0], colorsFromParameters=args.mrp[1])
    elif args.t == True:
        view.printToTerminal(tutorial.showTutorial())
    elif args.l == True:
        view.printToTerminal(leaderboard.showLeaderboard())
    elif args.k == True:
        gameLoopController.startGameMode("code")
    elif args.r == True:
        gameLoopController.startGameMode("guess")

    while True:
        menuOption = menu.showMenu()

        match menuOption:
            case "t":
                view.printToTerminal(tutorial.showTutorial())
            case "l":
                view.printToTerminal(leaderboard.showLeaderboard())
            case "k":
                gameLoopController.startGameMode("code")
            case "r":
                gameLoopController.startGameMode("guess")
            case "mk":
                gameLoopController.startGameMode("multiplayerCode")
            case "mr":
                gameLoopController.startGameMode("multiplayerGuess")
            case "q":
                exit()
            case _:
                view.printToTerminal(
                    "Etwas ist schief gelaufen bitte probiere es erneut"
                )


if __name__ == "__main__":
    gameLoopController = gameLoopControllerImpl()
    leaderboard = leaderboardImpl()
    menu = menuImpl()
    tutorial = tutorialImpl()
    view = viewImpl()
    main()




