from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

@app.route("/")
def index():
    return render_template('index.html')

# add support for GET and POST or figure out which one to use the most?
# figure out how to add authentication for the endpoints
# look into serverless tech

@app.route("/recordGameResults")
def recordGameResults():
    
    game_id = int(request.args.get('gameId'))
    player1_id = int(request.args.get('player1Id'))
    player2_id = int(request.args.get('player2Id'))
    winning_player_id = int(request.args.get('winningPlayerId'))

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO gameRecords (gameId, player1Id, player2Id, winningPlayerId) VALUES (%s,%s,%s,%s)", (game_id,player1_id,player2_id,winning_player_id) )
        conn.commit()
    except:
        return "Unable to save game data. Game results with that ID may already exist."

    return jsonify(
        gameId=game_id,
        player1Id=player1_id,
        player2Id=player2_id,
        winningPlayerId=winning_player_id
    )

@app.route("/getFirst50GameResults")    
def getFirst50GameResults():

    first_fifty_game_records = []

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM gameRecords LIMIT 50")
        game_records = cur.fetchall()
    except:
        return "Unable to retrieve game data for that gameId."
    
    for gameR in game_records:
        game = {}
        game['gameid'] = str(gameR[0])
        game['player1id'] = str(gameR[1])
        game['player2id'] = str(gameR[2])
        game['winningplayerid'] = str(gameR[3])
        first_fifty_game_records.append(game)
    
    return jsonify(first_fifty_game_records)

@app.route("/getGameResults")
def getGameResults():

    game_id_str = request.args.get('gameId')

    game_record = None

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM gameRecords WHERE gameId=%s", game_id_str)
        game_record = cur.fetchone()
    except:
        return "Unable to retrieve game data for that gameId."
    
    if not game_record:
        return "No game data exists for that gameId. The gameId may not exist."

    return jsonify(
        gameId=game_record[0],
        player1Id=game_record[1],
        player2Id=game_record[2],
        winningPlayerId=game_record[3]
    )

@app.route("/getAllPlayers")
def getAllPlayers():

    player_ids = []
    all_player_ids = None

    try:
        cur = conn.cursor()
        cur.execute("SELECT player1id,player2id FROM gameRecords")
        all_player_ids = cur.fetchall()
    except:
        return "Unable to retrieve all playerIds."

    if not player_ids:
       return "Could not find any records for any players."
    
    for id in player_ids:
       player_ids.append(id)
    
    return jsonify(all_player_ids)

@app.route("/getPlayerResults")
def getPlayerResults():

    player_id_str = request.args.get('playerId')

    game_records = None

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM gameRecords WHERE player1Id=%s OR player2Id=%s", (player_id_str,player_id_str))
        game_records = cur.fetchall()
    except:
        return "Unable to select game data for that playerId."

    if not game_records:
        return "No player results exist for that playerId. The playerId may not exist."

    all_game_records = []
    
    for gameR in game_records:
        game = {}
        game['gameid'] = str(gameR[0])
        game['player1id'] = str(gameR[1])
        game['player2id'] = str(gameR[2])
        game['winningplayerid'] = str(gameR[3])
        all_game_records.append(game)
    
    return jsonify(all_game_records)