# shrine-leaderboard

This is a heroku app for a contrived leaderboard for a make-believe ping-pong game. It's written with a python backend and has a crude frontend written in javascript and html.

This project can be started up just like any other heroku app.

The main python entrypoint is app.py.

The main API endpoint is 'recordGameResults'.

When a game ends, that 'recordGameResults' API endpoint should be called, providing it with the gameId, the player1Id, the player2Id, and the winningPlayerId.

The database schema is contained in schema.sql

The player rankings need to be calculated prior to use. To calculate the rankings, the API endpoint is '/computerPlayerRankings'. These rankings are stored in the table playerRanks.
