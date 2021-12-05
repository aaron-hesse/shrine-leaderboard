DROP TABLE gameRecords;
DROP TABLE eloScores;

CREATE TABLE gameRecords (
    gameId INT PRIMARY KEY,
    player1Id INT,
    player2Id INT,
    winningPlayerId INT
);

CREATE TABLE eloScores (
    playerId INT PRIMARY KEY,
    eloScore INT
);