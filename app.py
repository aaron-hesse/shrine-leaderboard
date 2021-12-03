from flask import Flask
from flask import request
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

# presumably the game client just calls a single api endpoint with all the information.
# then write the information to the database (postgres)

@app.route("/recordGameResults")
def recordGameResults():
    
    gameId = request.args.get('gameId')
    player1Id = request.args.get('player1Id')
    player2Id = request.args.get('player2Id')
    winningPlayerId = request.args.get('winningPlayerId')

    msg = "gameid type is: " + str(type(gameId) is str)

    #conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    #msg = "(recordGameResults): INSERTING the following information: " + gameId + " " + " player1Id: " + player1Id + " player2Id: " + player2Id + " winningPlayerId: " + winningPlayerId
    #cur = conn.cursor()
    #cur.execute("INSERT INTO gameRecords (gameId, player1Id, player2Id, winningPlayerId) VALUES (?,?,?,?)", (gameId,player1Id,player2Id,winningPlayerId) )
    #conn.commit()
    #conn.close()

    return msg