#this file contains the web application
from flask import Flask, render_template, request, flash, redirect, jsonify
#to display the template we need the render_template function
import config, csv
from binance.client import Client
#to import constants like SIDE_BUY, etc
from binance.enums import *
import pandas as pd
from patterns import patterns
import talib
import numpy


#our app is a flask object
app = Flask(__name__)
#in flask when using forms we need to give a secret key
#it could be defined in config
app.secret_key = 'fhfahflsdkaçlfhafsdkhfdshfdfoeurieubdk'

client = Client(config.API_KEY, config.API_SECRET, tld="com")

#define some routes and a function to call
#when that route is accessed from the browser
@app.route('/')
def index():
    title = 'Binance Trading Bot v2'
    account = client.get_account()
    balances = account['balances']

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols'] #let's pass it to the template too

    #taken from the trading bot v1 app. This allow to maintain current pattern.
    pattern = request.args.get('pattern',None)
    
    return render_template('index.html', title=title, my_balances = balances, symbols=symbols, patterns=patterns,current_pattern = pattern)
    #by default flask searches in the templates directory
    #we can pass variables and display them in the html file using {{}}

#buy endpoint. By default flask doesn't allow 'Post'
#methods no endpoint. We have to specify that they are allowed if its a post request from a form
@app.route('/buy', methods=['POST'])
def buy():
    try:
        order = client.create_order(
            #this is how to input variables from 
            #templaste forms....
            #print(request.form)
            symbol=request.form['symbol'],
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=request.form['quantity'])
    except Exception as e:
        #flask allows to send messages using flash(message,category)
        flash(e.message,"error")
    return redirect('/')
    #we return a redirect to /

#sell endpoint
@app.route('/sell', methods=['POST'])
def sell():
    try:
        order = client.create_order(
            #this is how to input variables from 
            #templaste forms....
            #print(request.form)
            symbol=request.form['symbol'],
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=request.form['quantity'])
    except Exception as e:
        #flask allows to send messages using flash(message,category)
        flash(e.message,"error")
    return redirect('/')
    #we return a redirect to /

#settings endpoint -> maybe to store settings in a database
@app.route('/settings')
def settings():
    return 'settings'

@app.route('/exchange-info',methods=['POST'])
def exchangeInfo():
    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

    for pair in symbols:
        print(pair['symbol'])
        csvfile = open('datasets/daily/{}.csv'.format(pair['symbol']),'w',newline='')
        candlestick_writer = csv.writer(csvfile,delimiter = ',')
        candlesticks = client.get_historical_klines("{}".format(pair['symbol']), Client.KLINE_INTERVAL_1DAY,"1 Jan, 2012","24 Aug, 2020")  
        
        str1 = ['Time','Open','High','Low','Close','Volume','CloseTime','QuoteVolume','NumberOfTrades','TBBase','TBQuote','Ignored']
        candlestick_writer.writerow(str1)
        for candlestick in candlesticks:
            candlestick_writer.writerow(candlestick)
            print(candlestick)
        csvfile.close()

    return redirect('/')
    #we return a redirect to /

@app.route('/candlestick-patterns',methods=['POST'])
def candlestickPatterns():
    print('Candlestick patterns detection')
    pattern = request.form['pattern']
    print(pattern)

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']
    stocks = {}
   

    pattern_function = getattr(talib, pattern)
    
    for pair in symbols:
    
        df = pd.read_csv('datasets/daily/{}.csv'.format(pair['symbol']))
        
        
        try:
            result = pattern_function(df['Open'],df['High'],df['Low'],df['Close'])
            
            last = result.tail(1).values[0]
            
            if last > 0:
                stocks[pair['symbol']]= 'bullish'
            elif last < 0:
                stocks[pair['symbol']] = 'bearish'
            else:
                stocks[pair['symbol']] = None
                #print("{} triggered {}".format(stockspair['symbol'], pattern))
            if stocks[pair['symbol']] != None:
                print("{} triggered {} -> {}".format(pair['symbol'],pattern,stocks[pair['symbol']]))
        except:
            pass
    #return render_template('index.html', patterns=patterns, stocks=stocks, current_pattern = pattern)





    return redirect('/')
#set FLASK_APP = app.py
#set FLASK_ENV=development
#flask run
#it may be necessary to create a virtual environment:
# $ py -3 -m venv venv
# $ venv\scripts\activate
#and install the requirements on that virtual environment(?)
#on flask we can make the browser refresh automatically
#activating the debug mode with the set FLASK_ENV=development
#instruction

@app.route('/history')
def history():
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY,"1 Jan, 2012","24 Aug, 2020") 
    
    #empty list
    processed_candlesticks = []

    for data in candlesticks:
        #since this is a python dictionary and not
        #a javascript object, the keys have ""
        candlestick = {
            "time": data[0]/1000, #binance data comes with miliseconds
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4] 
        }
    #this will give us a diferent structure to the data
    #instead of a list of lists now we will have a list of objcets
        processed_candlesticks.append(candlestick)
    
    #os lightweights charts do trading view want a unix timestamp
    
    return jsonify(processed_candlesticks)


@app.route('/SMA100',methods=['POST'])
def crossMA():
    print('checking for MA100 cross')

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']
    stocks = {}
    
    for pair in symbols:
    
        df = pd.read_csv('datasets/daily/{}.csv'.format(pair['symbol']))
        array = df.to_numpy()
        SMA100 = talib.EMA(array, timeperiod=100)
        
        print("{} -> {} SMA: {}".format(pair['symbol'],df['Close'].tail(1),SMA100))
        
        try:
            openval0 = df['Open'].tail(1)
            highval0 = df['High'].tail(1)
            lowval0 = df['Low'].tail(1)
            closeval0 = df['Close'].tail(1)
            openval1 = df['Open'].tail(2)
            highval1 = df['High'].tail(2)
            lowval1 = df['Low'].tail(2)
            close1 = df['Close'].tail(2)
            
            if closeval0 > SMA100 and closeval1 < SMA100 :
                stocks[pair['symbol']]= 'cross up'
            elif closeval0 < SMA100 and closeval1 > SMA100:
                stocks[pair['symbol']] = 'cross down'
            else:
                stocks[pair['symbol']] = None
                #print("{} triggered {}".format(stockspair['symbol'], pattern))
            if stocks[pair['symbol']] != None:
                print("{} triggered cross -> {}".format(pair['symbol'],stocks[pair['symbol']]))
        except:
            pass
    #return render_template('index.html', patterns=patterns, stocks=stocks, current_pattern = pattern)





    return redirect('/')