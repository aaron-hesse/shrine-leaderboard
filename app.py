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
    
    game_id = int(request.args.get('gameId'))
    player1_id = int(request.args.get('player1Id'))
    player2_id = int(request.args.get('player2Id'))
    winning_player_id = int(request.args.get('winningPlayerId'))

    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO gameRecords (gameId, player1Id, player2Id, winningPlayerId) VALUES (%s,%s,%s,%s)", (gameId,player1Id,player2Id,winningPlayerId) )
        conn.commit()
    except:
        return "Unable to save game data. Game results with that ID may already exist."

    return jsonify(
        gameId=gameId,
        player1Id=player1Id,
        player2Id=player2Id,
        winningPlayerId=winningPlayerId
    )

@app.route("/getGameResults")
def getGameResults():

    game_id_str = request.args.get('gameId')

    cur = conn.cursor()
    cur.execute("SELECT * FROM gameRecords WHERE gameId=%s", game_id_str)
    game_record = cur.fetchone()

    return jsonify(
        gameId=game_record[0],
        player1Id=game_record[1],
        player2Id=game_record[2],
        winningPlayerId=game_record[3]
    )

@app.route("/getPlayerResults")
def getPlayerResults():

    player_id_str = request.args.get('playerId')

    cur = conn.cursor()
    cur.execute("SELECT * FROM gameRecords WHERE player1Id=%s OR player2Id=%s", (player_id_str,player_id_str))
    game_records = cur.fetchall()

    all_game_records = []
    
    for gameR in game_records:
        game = {}
        game['gameid'] = str(gameR[0])
        game['player1id'] = str(gameR[1])
        game['player2id'] = str(gameR[2])
        game['winningplayerid'] = str(gameR[3])
        all_game_records.append(game)
    
    return jsonify(all_game_records)