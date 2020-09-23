import numpy
import talib
from numpy import genfromtxt
#we want to build a numpy array from a csv file
#->generate an array of numpy arrays
my_data = genfromtxt('15minBTCUSDT.csv',delimiter = ',')
print(my_data)
#it generates an array of arrays -- each row is a candle --

#this is the numpy syntax to extract the 4th column, that has 
#the closing price information
close = my_data[:,4]
print(close)

#close = numpy.random.random(100)
#moving_average = talib.SMA(close, timeperiod = 10)
#print(moving_average)

rsi = talib.RSI(close)
print(rsi)