DROP TABLE gameRecords;
DROP TABLE playerRanks;

CREATE TABLE gameRecords (
    gameId INT PRIMARY KEY,
    player1Id INT,
    player2Id INT,
    winningPlayerId INT
);

CREATE TABLE playerRanks (
    playerId INT PRIMARY KEY,
    winPercent DECIMAL
);