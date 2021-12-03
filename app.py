from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

# presumably the game client just calls a single api endpoint with all the information.

@app.route("/recordGameResults")
def recordGameResults():
    gameId = request.args.get('gameId')
    player1Name = request.args.get('player1Name')
    player2Name = request.args.get('player2Name')
    winningPlayer = request.args.get('winningPlayer')
    return "recordGameResults: " + gameId + " " + " player1Name: " + player1Name