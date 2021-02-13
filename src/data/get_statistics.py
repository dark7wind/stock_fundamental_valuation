import csv
import os
from definitions import ROOT_DIR
from yahoo_fin.stock_info import *

TICKERS_DIR = os.path.join(ROOT_DIR, 'data/tickers/')
FUNDAMENTAL_DIR = os.path.join(ROOT_DIR, 'data/fundamental/statistics/')

## dow
file_ticker = 'dow_tickers.csv'
file_statistics = 'statistics_dow.csv'
tickers_dow = list()
with open(TICKERS_DIR+file_ticker, newline='') as csvfile:
    ticker_reader = csv.reader(csvfile, delimiter=',')
    for row in ticker_reader:
        tickers_dow.append(row)

statistics_total = pd.DataFrame()
for ticker in tickers_dow[0]:
    statistics = get_stats(ticker)
    statistics = statistics.set_index(['Attribute'])
    statistics = statistics.T
    statistics = statistics.reset_index()
    statistics.drop(columns=['index'], inplace=True)
    statistics['ticker'] = ticker
    statistics_total = statistics_total.append(statistics, ignore_index=True)

statistics_total.to_csv(FUNDAMENTAL_DIR+file_statistics, index=False)

