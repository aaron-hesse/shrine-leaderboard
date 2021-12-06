# shrine-leaderboard

This is a heroku app for a contrived leaderboard for a make-believe ping-pong game. It's written with a python backend and has a crude frontend written in javascript and html.

This project can be started up just like any other heroku app.

The main python entrypoint is app.py.

If you want to run this locally, you'd need to do some work to connect the python3 script to the backend (and on heroku the original db was PostgreSQL).

The main API endpoint is 'recordGameResults'.

When a game ends, that 'recordGameResults' API endpoint should be called, providing it with the gameId, the player1Id, the player2Id, and the winningPlayerId.

The database schema is contained in schema.sql

The player rankings need to be calculated prior to use. To calculate the rankings, the API endpoint is '/computerPlayerRankings'. These rankings are stored in the table playerRanks.

Examples of the main api endpoints and the index page (for the original version hosted on heroku):

https://shrine-realpython-example-app.herokuapp.com/
https://shrine-realpython-example-app.herokuapp.com/getGameResults?gameId=1
https://shrine-realpython-example-app.herokuapp.com/getPlayerResults?playerId=548
https://shrine-realpython-example-app.herokuapp.com/getFirst50GameResults
https://shrine-realpython-example-app.herokuapp.com/getAllPlayers
https://shrine-realpython-example-app.herokuapp.com/computePlayerRankings
https://shrine-realpython-example-app.herokuapp.com/getTop50Players

All of the API endpoints return JSON objects or arrays of JSON objects.
