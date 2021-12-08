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

function getPlayerResults(playerId) {
    makeBackendAPIRequest("https://shrine-realpython-example-app.herokuapp.com/getPlayerResults?playerId=548", updateGameResultsTable)
}

function getAllPlayers() {
    makeBackendAPIRequest("https://shrine-realpython-example-app.herokuapp.com/getAllPlayers", updatePlayerTable)
}

function emptyTable(tableName) {
    var table = document.getElementById(tableName);
    var rowCount = table.rows.length;
    var rowIndex = 1;
    for (var i = rowIndex; i < rowCount; i++) {
        table.deleteRow(rowIndex);
    }
}

function emptyPlayerTable() {
    emptyTable('playerTable')
}

function emptyGameResultsTable() {
    emptyTable('gameResultsTable')
}

function emptyRankedPlayersTable() {
    emptyTable('top50PlayerTable')
}

function updatePlayerTable(tableData) {

    emptyPlayerTable()

    // The JSON object returned by getAllPlayers is simply an array, there's no key->value mapping

    for (var i = 0; i < tableData.length; i++) {
        var obj = tableData[i];
        var newRow = document.getElementById('playerTable').insertRow();
        newRow.innerHTML += "<td>" + obj + "</td>"
        console.log('obj: ' + obj)
    }
}

function updateGameResultsTable(tableData) {

    emptyGameResultsTable()

    for (var i = 0; i < tableData.length; i++) {
        var obj = tableData[i];
        var newRow = document.getElementById('gameResultsTable').insertRow();
        newRow.innerHTML += "<td>" + obj['gameid'] + "</td>"
        newRow.innerHTML += "<td>" + obj['player1id'] + "</td>"
        newRow.innerHTML += "<td>" + obj['player2id'] + "</td>"
        newRow.innerHTML += "<td>" + obj['winningPlayerid'] + "</td>"
    }
}

function updateRankedPlayersTable(tableData) {

    emptyRankedPlayersTable()
    
    var rank = 1
    for (var i = 0; i < tableData.length; i++) {

        var obj = tableData[i];
        var newRow = document.getElementById('top50PlayerTable').insertRow();
        var playerId = ""
        var winPercentage = ""

        Object.keys(obj).forEach(function (key) {
            playerId = obj['playerid']
            winPercentage = obj['winpercentage']
        })
        
        newRow.innerHTML = "<td>" + rank + "</td><td>" + playerId + "</td><td>" + winPercentage + "</td>"
        rank += 1
    }
}

function getFirst50GameResults() {
    makeBackendAPIRequest("https://shrine-realpython-example-app.herokuapp.com/getFirst50GameResults", updateGameResultsTable)
}

function getTop50Players() {
    makeBackendAPIRequest("https://shrine-realpython-example-app.herokuapp.com/getTop50Players", updateRankedPlayersTable)
}