
const TOP_FIFTY_PLAYER_TABLE_NAME = "top50PlayerTable"
const ALL_PLAYERS_TABLE_NAME = "playerTable"
const FIRST_FIFTY_GAME_RESULTS_TABLE_NAME = "gameResultsTable"
const BACKEND_SERVER_URL = "https://shrine-realpython-example-app.herokuapp.com"

function makeBackendAPIRequest(url, callback) {
    let request = new XMLHttpRequest();
    request.open("GET", url)
    request.send();
    request.onload = () => {
        console.log(request);
        if (request.status === 200){
            parsedJSON = JSON.parse(request.response) 
            console.log(parsedJSON)
            callback(parsedJSON)
        } else {
            console.log(`error ${request.status} ${request.statusText}`)
            return false
        }
    }
}

function getAllPlayers() {
    makeBackendAPIRequest(BACKEND_SERVER_URL + "/getAllPlayers", updatePlayerTable)
}

function getFirst50GameResults() {
    makeBackendAPIRequest(BACKEND_SERVER_URL + "/getFirst50GameResults", updateGameResultsTable)
}

function getTop50Players() {
    makeBackendAPIRequest(BACKEND_SERVER_URL + "/getTop50Players", updateRankedPlayersTable)
}

function emptyTable(tableName) {
    const table = getTable(tableName);
    const rowCount = table.rows.length;
    for (var i = 1; i < rowCount; i++)
        table.deleteRow(1)
}

function getTable(tableName) {
    return document.getElementById(tableName);
}

function emptyPlayerTable() {
    emptyTable(ALL_PLAYERS_TABLE_NAME)
}

function emptyGameResultsTable() {
    emptyTable(FIRST_FIFTY_GAME_RESULTS_TABLE_NAME)
}

function emptyRankedPlayersTable() {
    emptyTable(TOP_FIFTY_PLAYER_TABLE_NAME)
}

function updatePlayerTable(tableData) {

    emptyPlayerTable()

    // The JSON object returned by getAllPlayers is simply an array, there's no key->value mapping

    for (var i = 0; i < tableData.length; i++) {
        const obj = tableData[i]
        var newRow = getTable('playerTable').insertRow()
        newRow.innerHTML += "<td>" + obj + "</td>"
        console.log('obj: ' + obj)
    }
}

function updateGameResultsTable(tableData) {

    emptyGameResultsTable()

    for (var i = 0; i < tableData.length; i++) {
        const obj = tableData[i]
        var newRow = getTable('gameResultsTable').insertRow()
        newRow.innerHTML += "<td>" + obj['gameid'] + "</td>"
        newRow.innerHTML += "<td>" + obj['player1id'] + "</td>"
        newRow.innerHTML += "<td>" + obj['player1score'] + "</td>"
        newRow.innerHTML += "<td>" + obj['player2id'] + "</td>"
        newRow.innerHTML += "<td>" + obj['player2score'] + "</td>"
        newRow.innerHTML += "<td>" + obj['winningPlayerid'] + "</td>"
    }
}

function updateRankedPlayersTable(tableData) {

    emptyRankedPlayersTable()
    
    var rank = 1
    for (var i = 0; i < tableData.length; i++) {
        
        var playerId = ""
        var winPercentage = ""
        const obj = tableData[i]
        Object.keys(obj).forEach(function (key) {
            playerId = obj['playerid']
            winCount = obj['wincount']
            winPercentage = obj['winpercent']
        })
        
        var newRow = getTable('top50PlayerTable').insertRow()
        newRow.innerHTML = "<td>" + rank + "</td><td>" + playerId + "</td><td>" + winCount + "</td><td>" + winPercentage + "</td>"
        rank++
    }
}