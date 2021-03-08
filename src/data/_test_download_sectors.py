import yfinance as yf
import MySQLdb as mdb
import os
import yaml
import datetime

tickerdata = yf.Ticker('TYL') #the tickersymbol for Tesla
print (tickerdata.info['industry'])
1