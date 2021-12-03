from flask import Flask
from flask import request
from flask import jsonify

import os
import psycopg2
import json

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

@app.route("/")
def index():
    return "Hello World!"

# add support for GET and POST or figure out which one to use the most?
# figure out how to add authentication for the endpoints
# look into serverless tech

@app.route("/recordGameResults")
def recordGameResults():
    
    gameId = int(request.args.get('gameId'))
    player1Id = int(request.args.get('player1Id'))
    player2Id = int(request.args.get('player2Id'))
    winningPlayerId = int(request.args.get('winningPlayerId'))

    cur = conn.cursor()
    cur.execute("INSERT INTO gameRecords (gameId, player1Id, player2Id, winningPlayerId) VALUES (%s,%s,%s,%s)", (gameId,player1Id,player2Id,winningPlayerId) )
    conn.commit()

    return jsonify(
        gameid=gameId,
        player1id=player1Id,
        player2id=player2Id,
        winningplayerid=winningPlayerId
    )

@app.route("/getGameResults")
def getGameResults():

    gameIdStr = request.args.get('gameId')

    cur = conn.cursor()
    cur.execute("SELECT * FROM gameRecords WHERE gameId=%s", gameIdStr)
    gameRecord = cur.fetchone()

    return jsonify(
        gameid=gameRecord[0],
        player1id=gameRecord[1],
        player2id=gameRecord[2],
        winningplayerid=gameRecord[3]
    )

@app.route("/getPlayerResults")
def getPlayerResults():

    playerIdStr = request.args.get('playerId')

    cur = conn.cursor()
    cur.execute("SELECT * FROM gameRecords WHERE player1Id=%s OR player2Id=%s", (playerIdStr,playerIdStr))
    gameRecords = cur.fetchall()

    #allGameRecords = ""
    #allGameRecords += "{"
    #for game in gameRecords:  
      #  allGameRecords += "{"
      #  allGameRecords += " 'gameid': " + str(game[0]) + ","
     #   allGameRecords += " 'player1id': " + str(game[1]) + ","
    #    allGameRecords += " 'player2id': " + str(game[2]) + ","
    #    allGameRecords += " 'winningPlayerid': " + str(game[3])
    #    allGameRecords += "}"
    #allGameRecords += "}"

    allGameRecords = []
    game = {}
    for gameR in gameRecords:
        game['gameid'] = str(gameR[0])
        game['player1id'] = str(gameR[1])
        game['player2id'] = str(gameR[2])
        game['winningplayerid'] = str(gameR[3])
        allGameRecords.append(game)
    
    return allGameRecords