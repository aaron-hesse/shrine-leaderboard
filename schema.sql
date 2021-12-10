DROP TABLE gameRecords;
DROP TABLE playerRanks;

CREATE TABLE gameRecords (
    gameId INT PRIMARY KEY,
    player1Id INT,
    player1Score INT,
    player2Id INT,
    player2Score INT,
    winningPlayerId INT
);

CREATE TABLE playerRanks (
    playerId INT PRIMARY KEY,
    totalScore INT,
    winCount INT,
    winPercent INT
);