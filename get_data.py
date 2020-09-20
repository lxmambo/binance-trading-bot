import config, csv
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)

#Show all tickers/trading pairs available
#prices = client.get_all_tickers()
#for price in prices:
#    print(price)

#used in the part of the code to save a file with stream data
#candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_15MINUTE)

csvfile = open('daily.csv','w',newline='')
candlestick_writer = csv.writer(csvfile,delimiter = ',')

#the code below is to write the stream in a csv file
#for candlestick in candles:
#    print(candlestick)
#    candlestick_writer.writerow(candlestick)
#print(len(candles))

candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY,"1 Jan, 2012","26 Aug, 2020")
for candlestick in candlesticks:
    candlestick_writer.writerow(candlestick)
csvfile.close()