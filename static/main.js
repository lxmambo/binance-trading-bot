//Javascript websocket object
var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@trade");

var tradeDiv = document.getElementById("trades");

//When we receive a message, execute this function
binanceSocket.onmessage = function(event) {
    // console.log(event.data);
    //the message is a JSON stream, but we want
    //to treat it as an object ->
    var messageObject = JSON.parse(event.data);
    //tradeDiv.append(messageObject.p);
    tradeDiv.textContent = messageObject.p;
    //displaying the price atribute
}


