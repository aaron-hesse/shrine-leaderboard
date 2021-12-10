const TOP_FIFTY_PLAYER_TABLE_NAME = "top50PlayerTable"
const ALL_PLAYERS_TABLE_NAME = "playerTable"
const FIRST_FIFTY_GAME_RESULTS_TABLE_NAME = "gameResultsTable"
const BACKEND_SERVER_URL = "https://shrine-realpython-example-app.herokuapp.com"

const GET_ALL_PLAYERS_API = "/getAllPlayers"
const GET_FIRST_FIFTY_RESULTS = "/getFirst50GameResults"
const GET_TOP_FIFTY_PLAYERS = "/getTop50Players"

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
    makeBackendAPIRequest(BACKEND_SERVER_URL + GET_ALL_PLAYERS_API, updatePlayerTable)
}

function getFirst50GameResults() {
    makeBackendAPIRequest(BACKEND_SERVER_URL + GET_FIRST_FIFTY_RESULTS, updateGameResultsTable)
}

function getTop50Players() {
    makeBackendAPIRequest(BACKEND_SERVER_URL + GET_TOP_FIFTY_PLAYERS, updateRankedPlayersTable)
}

function emptyTable(tableName) {

    let table = getTable(tableName)
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

    for (var i = 0; i < tableData.length; i++) {
        var newRow = getTable('playerTable').insertRow()
        newRow.innerHTML += "<td>" + tableData[i] + "</td>"
    }
}

function updateGameResultsTable(tableData) {

    emptyGameResultsTable()

    for (var i = 0; i < tableData.length; i++) {
        var newRow = getTable('gameResultsTable').insertRow()
        Object.values(tableData[i]).forEach(value => {
            newRow.innerHTML += "<td>" + value + "</td>"
        });
    }
}

function updateRankedPlayersTable(tableData) {

    emptyRankedPlayersTable()
    
    var rank = 1
    for (var i = 0; i < tableData.length; i++) {
        const obj = tableData[i]
        var newRow = getTable(TOP_FIFTY_PLAYER_TABLE_NAME).insertRow()
        newRow.innerHTML = "<td>" + rank + "</td><td>" + obj['playerid'] + "</td><td>" + obj['totalscore'] + "</td><td>" + obj['wincount'] + "</td><td>" + obj['winpercent'] + "</td>"
        rank++
    }
}