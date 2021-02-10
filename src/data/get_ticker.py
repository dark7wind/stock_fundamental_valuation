import csv
import os
from definitions import ROOT_DIR
from yahoo_fin.stock_info import *

TICKERS_DIR = os.path.join(ROOT_DIR, 'data/tickers/')

sp500_tickers = tickers_sp500()
file_name = 'sp500_tickers.csv'
with open(TICKERS_DIR+file_name, mode='w') as ticker_file:
    ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    ticker_writer.writerow(sp500_tickers)

dow_tickers = tickers_dow()
file_name = 'dow_tickers.csv'
with open(TICKERS_DIR+file_name, mode='w') as ticker_file:
    ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    ticker_writer.writerow(dow_tickers)

nasdaq_tickers = tickers_nasdaq()
file_name = 'nasdaq_tickers.csv'
with open(TICKERS_DIR+file_name, mode='w') as ticker_file:
    ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    ticker_writer.writerow(nasdaq_tickers)

other_tickers = tickers_other()
file_name = 'other_tickers.csv'
with open(TICKERS_DIR+file_name, mode='w') as ticker_file:
    ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    ticker_writer.writerow(other_tickers)

1