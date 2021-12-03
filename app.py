from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

# presumably the game client just calls a single api endpoint with all the information.

@app.route("/recordGameResults")
def recordGameResults():
    gameId = request.args.get('gameId')
    player1Id = request.args.get('player1Id')
    player2Id = request.args.get('player2Id')
    winningPlayerId = request.args.get('winningPlayerId')
    return "recordGameResults: " + gameId + " " + " player1Id: " + player1Id + " player2Id: " + player2Id + " winningPlayerId: " + winningPlayerId