import numpy
import talib
#we want to build a numpy array from a csv file
#->generate an array of numpy arrays
from numpy import genfromtxt

my_data = genfromtxt('15minBTCUSDT.csv',delimiter = ',')
print(my_data)

close = my_data[:,4]
print(close)

#close = numpy.random.random(100)
#moving_average = talib.SMA(close, timeperiod = 10)
#print(moving_average)

rsi = talib.RSI(close)
print(rsi)