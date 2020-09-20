var chart = LightweightCharts.createChart(document.getElementById('chart'), {
	width: 600,
  height: 300,
	layout: {
		backgroundColor: '#1c223b',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	rightPriceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
});

var candleSeries = chart.addCandlestickSeries({
  upColor: '#00ff00',
  downColor: '#ff0000',
  borderDownColor: '#ff0000',
  borderUpColor: '#00ff00',
  wickDownColor: '#ff0000',
  wickUpColor: '#00ff00',
});

//The data must come from the back end. We need to Fetch it.
fetch('http://localhost:5000/history')
	.then((r) => r.json())
	.then((response) => {
		console.log(response)
		candleSeries.setData(response);
	})

var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_1d");

binanceSocket.onmensage = function(event){
	
//we are going to retrieve the message object coming backgroundColor
	var message = JSON.parse(event.data);
	var candlestick = message.k;
	console.log(candlestick)
	//update function from lightweight. if time is the same, it updates
	candleSeries.upadate({
		time:candlestick.t/1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})
}