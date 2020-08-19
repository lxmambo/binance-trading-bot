//socket objec
var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@trade");

var tradeDiv = document.getElementById("trades");

binanceSocket.onmessage = function(event) {
    console.log(event.data);
    var messageObject = JSON.parse(event.data);
    //tradeDiv.append(messageObject.p);
    tradeDiv.textContent = messageObject.p;
}
