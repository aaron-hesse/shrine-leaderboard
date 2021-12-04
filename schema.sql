DROP TABLE gameRecords;

CREATE TABLE gameRecords (
    gameId INT PRIMARY KEY,
    player1Id INT,
    player2Id INT,
    winningPlayerId INT
);