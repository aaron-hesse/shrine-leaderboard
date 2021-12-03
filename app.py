from flask import Flask
from flask import request
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/recordGameResults")
def recordGameResults():
    
    gameId = int(request.args.get('gameId'))
    player1Id = int(request.args.get('player1Id'))
    player2Id = int(request.args.get('player2Id'))
    winningPlayerId = int(request.args.get('winningPlayerId'))

    cur = conn.cursor()
    cur.execute("INSERT INTO gameRecords (gameId, player1Id, player2Id, winningPlayerId) VALUES (%s,%s,%s,%s)", (gameId,player1Id,player2Id,winningPlayerId) )
    conn.commit()

    return "Wrote the game info into the table."

@app.route("/getGameResults")
def getGameResults():

    gameIdStr = request.args.get('gameId')
    gameId = int(gameIdStr)

    cur = conn.cursor()
    cur.execute("SELECT * FROM gameRecords WHERE gameId=%s", gameId)
    gameRecord = cur.fetchone()


    return "gameId: " + gameRecord[0] + " player1Id: " + gameRecord[1]

