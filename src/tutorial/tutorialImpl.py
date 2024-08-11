from src.tutorial.tutorialInterface import tutorialInterface


class tutorialImpl(tutorialInterface):
    tutorialText: str = """
-------------------------------------- SPIELREGELN --------------------------------------\n
Superhirn ist ein Strategiespiel für zwei Spieler,bei dem einer der Kodierer 
und der andere der Rater ist. Das Spiel beginnt damit, dass der Kodierer eine 
geheime Kombination aus mehreren farbigen Pins wählt, normalerweise vier Farben
aus einer Auswahl von sechs bis acht. Das Ziel des Raters ist es,
diesen geheimen Farbcode durch wiederholtes Raten zu entschlüsseln.\n\n
In jeder Runde stellt der Rater eine Kombination von Farben auf und erhält vom 
Kodierer Feedback. Für jede Farbe, die an der richtigen Position ist, gibt es einen 
schwarzen Pin, und für jede richtige Farbe an der falschen Position einen weißen Pin. 
Dieses Feedback hilft dem Rater, seine nächsten Versuche anzupassen und sich dem Farbcode 
Schritt für Schritt anzunähern. Der Rater gewinnt, wenn er den Farbcode innerhalb 
einer bestimmten Anzahl von Versuchen korrekt errät. Gelingt dies nicht, gewinnt der
Kodierer.\n\n
Wenn du der Kodierer bist, wählst du einen geheimen Farbcode und gibst nach jedem 
Versuch des Raters präzises Feedback in Form von schwarzen und weißen Pins. Es ist wichtig,
die Versuche und das gegebene Feedback zu notieren, um die Übersicht zu behalten. 
Wenn du der Rater bist, stellst du eine erste Kombination auf und wartest auf das Feedback
des Kodierers. Nutze dieses Feedback, um deine nächsten Versuche strategisch anzupassen 
und den genauen Farbcode durch Ausschluss und Kombination zu entschlüsseln.\n\n
Viel Spaß beim Spielen!\n
-----------------------------------------------------------------------------------------"""

    def showTutorial(self) -> str:
        return self.tutorialText
