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

@app.route("/recordGameResults")
def recordGameResults():
    
    game_id = int(request.args.get('gameId'))
    player1_id = int(request.args.get('player1Id'))
    player1_score = int(request.args.get('player1score'))
    player2_id = int(request.args.get('player2Id'))
    player2_score = int(request.args.get('player2score'))
    winning_player_id = int(request.args.get('winningPlayerId'))

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO gameRecords (gameId, player1Id, player1score, player2Id, player2score, winningPlayerId) VALUES (%s,%s,%s,%s,%s,%s)", (game_id,player1_id,player1_score,player2_id,player2_score,winning_player_id) )
        conn.commit()
    except:
        return "Unable to save game data. Game results with that ID may already exist."

    return jsonify(
        gameId=game_id,
        player1Id=player1_id,
        player1Score=player1_score,
        player2Id=player2_id,
        player2Score=player2_score,
        winningPlayerId=winning_player_id
    )


@app.route("/getTop50Players")
def getTop50Players():

    top_fifty_players = []

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM playerRanks ORDER BY winpercent DESC LIMIT 50")
        top_fifty_players = cur.fetchall()
    except:
        return "Unable to retrieve data for top 50 players."

    playerRankList = []
    for playerRank in top_fifty_players:
        playerRankData = {}
        playerRankData['playerid'] = playerRank[0]
        playerRankData['totalscore'] = playerRank[1]
        playerRankData['wincount'] = playerRank[2]
        playerRankData['winpercent'] = "{:.0%}".format(float(playerRank[3]))
        playerRankList.append(playerRankData)

    return jsonify(playerRankList)


@app.route("/getFirst50GameResults")    
def getFirst50GameResults():

    first_fifty_game_records = []

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM gameRecords ORDER BY gameId ASC LIMIT 50")
        game_records = cur.fetchall()
    except:
        return "Unable to retrieve game data for first 50 games."

    for game_record in game_records:
        game = buildGameObjectFromGameRecord(game_record)
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
        player1_score=game_record[2],
        player2Id=game_record[3],
        player2_score=game_record[4],
        winningPlayerId=game_record[5]
    )

@app.route("/getAllPlayers")
def getAllPlayers():

    player_ids = []
    all_player_ids = None

    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT player1id,player2id FROM gameRecords")
        all_player_ids = cur.fetchall()
    except:
        return "Unable to retrieve all playerIds."

    if not all_player_ids:
       return "Could not find any records for any players."
    
    for row in all_player_ids:
       player_ids.append(row[0])
       player_ids.append(row[1])
    
    return jsonify(player_ids)

@app.route("/computePlayerRankings")
def computePlayerRankings():
    
    all_game_records = []

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM gamerecords")
        all_game_records = cur.fetchall()
    except:
        return "Unable to retrieve data from gamerecords."

    playerGameCountDict = {}
    playerWinCountDict = {}
    playerWinPercentDict = {}
    playerTotalScoreDict = {}
    
    for game_record in all_game_records:    
        buildPlayerRankingDictionaries(playerGameCountDict, playerWinCountDict, playerWinPercentDict, playerTotalScoreDict, game_record)

    print("playerGameCountDict: ")
    printDict(playerGameCountDict)
    print("playerWinCountDict: ")
    printDict(playerWinCountDict)
    print("playerWinPercentDict:")
    printDict(playerWinPercentDict)
    print("playerTotalScoreDict: ")
    printDict(playerTotalScoreDict)

    playerWinCount = 0
    cur = conn.cursor()
    for playerid in playerWinPercentDict:
        if playerid in playerWinCountDict:
            playerWinCount = playerWinCountDict[playerid]
        cur.execute("INSERT INTO playerRanks (playerId, totalScore, winCount, winPercent) VALUES (%s,%s,%s,%s) ON CONFLICT (playerId) DO UPDATE SET totalScore=excluded.totalScore, winPercent=excluded.winPercent, winCount=excluded.winCount", (playerid, playerTotalScoreDict[playerid], playerWinCount, playerWinPercentDict[playerid]))
        conn.commit()

    return jsonify(playerWinPercentDict)
    

@app.route("/getPlayerResults")
def getPlayerResults():

    player_id_str = request.args.get('playerId')
    game_records  = None

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM gameRecords WHERE player1Id=%s OR player2Id=%s", (player_id_str,player_id_str))
        game_records = cur.fetchall()
    except:
        return "Unable to select game data for that playerId."

    if not game_records:
        return "No player results exist for that playerId. The playerId may not exist."

    all_game_records = []
    for game_record in game_records:
        game = buildGameObjectFromGameRecord(game_record)
        all_game_records.append(game)
    
    return jsonify(all_game_records)

def buildPlayerRankingDictionaries(playerGameCountDict, playerWinCountDict, playerWinPercentDict, playerTotalScoreDict, game_record):

        # this code computes the win/loss ratio/percentage using three dicts
        # this should be changed to an ELO ranking system instead.

        player1id = str(game_record[1])
        player1score = str(game_record[2])
        player2id = str(game_record[3])
        player2score = str(game_record[4])
        winningPlayerId = str(game_record[5])

        print('player1score: ' + player1score)
        print('player2score: ' + player2score)

        if player1id in playerGameCountDict:
            playerGameCountDict[player1id] += 1
        else:
            playerGameCountDict[player1id] = 1

        if player2id in playerGameCountDict:
            playerGameCountDict[player2id] += 1
        else:
            playerGameCountDict[player2id] = 1

        if winningPlayerId in playerWinCountDict:
            playerWinCountDict[winningPlayerId] += 1
        else:
            playerWinCountDict[winningPlayerId] = 1

        if player1id in playerWinCountDict:
            playerWinPercentDict[player1id] = playerWinCountDict[player1id] / playerGameCountDict[player1id]
        else:
            playerWinPercentDict[player1id] = 0

        if player2id in playerWinCountDict:
            playerWinPercentDict[player2id] = playerWinCountDict[player2id] / playerGameCountDict[player1id]
        else:
            playerWinPercentDict[player2id] = 0

        if player1id in playerTotalScoreDict:
            playerTotalScoreDict[player1id] += int(player1score)
        else:
            playerTotalScoreDict[player1id] = int(player1score)

        if player2id in playerTotalScoreDict:
            playerTotalScoreDict[player2id] += int(player2score)
        else:
            playerTotalScoreDict[player2id] = int(player1score)

def buildGameObjectFromGameRecord(game_record):
    game = {}
    game['gameid'] = str(game_record[0])
    game['player1id'] = str(game_record[1])
    game['player1score'] = str(game_record[2])
    game['player2id'] = str(game_record[3])
    game['player2score'] = str(game_record[4])
    game['winningplayerid'] = str(game_record[5])

    print('game_record:')
    for entry in game_record:
        print(entry)

    print('game:')
    printDict(game)

    return game

def printDict(dict):
    for key, value in dict.items():
        print(key, ' : ', value)