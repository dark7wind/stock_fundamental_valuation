import csv
import os
from definitions import ROOT_DIR
from yahoo_fin.stock_info import *

pd.set_option('display.max_columns', None)

TICKERS_DIR = os.path.join(ROOT_DIR, 'data/tickers/')
FUNDAMENTAL_DIR = os.path.join(ROOT_DIR, 'data/fundamental/analysis_info/')


## dow
file_ticker = 'dow_tickers.csv'
file_analysts_info_total = 'analysis_info_dow.csv'
tickers_dow = list()
with open(TICKERS_DIR+file_ticker, newline='') as csvfile:
    ticker_reader = csv.reader(csvfile, delimiter=',')
    for row in ticker_reader:
        tickers_dow.append(row)

analysts_info_total = pd.DataFrame()
for ticker in tickers_dow[0]:
    analysts_info = get_analysts_info(ticker)


    analysts_info = analysts_info.T
    analysts_info = analysts_info.reset_index()
    analysts_info['ticker'] = ticker
    analysts_info_total = analysts_info_total.append(analysts_info, ignore_index=True)

analysts_info_total.to_csv(FUNDAMENTAL_DIR+file_analysts_info_total, index=False)

1