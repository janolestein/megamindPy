
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
import time
from os import linesep
from src.game.serverFeedbackHelper import serverFeedbackHelper
from src.view.viewImpl import viewImpl


# define handler class to handle requests
class RequestHandler(BaseHTTPRequestHandler):

    # GET-requests are ignored (only post is supported)
    def do_GET(self):
        self.send_response(405)  # Method Not Allowed
        self.end_headers()
        self.wfile.write(b"GET requests are not supported. Use POST.")

    # POST-requests are handled here
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            # try to load JSON
            data = json.loads(post_data.decode('utf-8'))
            print("Received POST request with data:", data)
            receivedData = data.copy()
            if data["gameid"] == 0:
                self.server.guesses = []
                self.server.correctPositions = []
                self.server.correctColors = []
                self.server.numTries = 0
                colorList = self.server.colors
                if self.server.selfCode == "y":
                    code = takeCodeFromUser(data["colors"], data["positions"], colorList)
                    self.server.feedbackHelper = serverFeedbackHelper(data["colors"], colorList, data["positions"],
                                                                      False, code)
                else:
                    self.server.feedbackHelper = serverFeedbackHelper(data["colors"], colorList, data["positions"],
                                                                      True, [])
                print(self.server.feedbackHelper.getCode())
                data["gameid"] = random.randint(1, 1000)
                self.server.gameid = data["gameid"]
                print(self.server.gameid)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(data)
                self.wfile.write(response.encode('utf-8'))
            elif data["gameid"] == self.server.gameid:
                codeList: list = [int(x) for x in data["value"]]
                feedback = self.server.feedbackHelper.giveFeedback(codeList)
                data["value"] = "8" * feedback[0] + "7" * feedback[1]
                self.server.guesses.append(codeList)
                self.server.correctPositions.append(feedback[0])
                self.server.correctColors.append(feedback[1])
                view = viewImpl()
                named_tuple = time.localtime()  # get struct_time
                time_string = time.strftime("%H:%M:%S", named_tuple)

                view.printGameBoard(
                    self.server.feedbackHelper.drawGameBoard(self.server.guesses, self.server.correctPositions,
                                                             self.server.correctColors, data["positions"], 10,
                                                             self.server.numTries, time_string))
                print("Code der geraten werden muss: " + str(self.server.feedbackHelper.getCode()) + linesep)
                print("Daten die in der Anfrage angekommen sind: " + linesep + str(receivedData) + linesep)
                print("Server kann mit CTRL+C beendet werden")

                self.server.numTries += 1
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps(data)
                self.wfile.write(response.encode('utf-8'))

        except ValueError as e:
            print("Value Error")
            self.send_response(400)  # Bad Request
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({"status": "error", "message": str(e)})
            self.wfile.write(response.encode('utf-8'))


class customServer(HTTPServer):
    def __init__(self, address, handler, colors: list, selfCode: str):
        self.feedbackHelper = object
        self.colors = colors
        self.gameid = ""
        self.selfCode = selfCode
        self.guesses: list = []
        self.correctPositions: list = []
        self.correctColors: list = []
        self.numTries = 0
        super().__init__(address, handler)


def startServer(colors: list, selfCode: str, ipaddress, port):
    if port == "":
        port = 8000
    else:
        port = int(port)
    # Define address and port of Server
    server_address = (ipaddress, port)  # empty string for localhost and port:8000
    # create instance of http-server and start it
    if ipaddress == "":
        ipaddress = "127.0.0.1"

    http_server = customServer(server_address, RequestHandler, colors, selfCode)
    try:

        print(f'Starting server on ip-address: {ipaddress} and port: {port}' + linesep)
        print("Warte auf Spieler..." + linesep)
        http_server.serve_forever()

    except KeyboardInterrupt:
        print('Server interrupted, shutting down...')
        http_server.socket.close()


def takeCodeFromUser(colorsNum, positions, colorList):
    colorsInUse = colorList[:int(colorsNum)]
    view = viewImpl()
    while True:
        code: str = view.takeInputFromUser(
            f"Bitte gib den Code ein der geraten werden soll. Mit {colorsNum} Farben und {positions} Stellen")
        if represents_int(code) == False:
            view.printToTerminal("Bitte gib eine Nummer ein")
            continue
        elif not len(code) == int(positions):
            view.printToTerminal("Bitte gib eine " + positions + " stellige Zahl ein")
            continue
        else:
            codeList: list = [int(x) for x in code]
            for elem in codeList:
                if not elem in colorsInUse:
                    view.printToTerminal(
                        "Der Code enthält Farben die nicht in der momentanten Farbauswahl enthalten sind, bitte gib einen anderen Code ein")
                    break
            else:
                return codeList


def represents_int(s) -> bool:
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True
