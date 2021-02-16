import csv
import os
from definitions import ROOT_DIR
from yahoo_fin.stock_info import *

TICKERS_DIR = os.path.join(ROOT_DIR, 'data/tickers/')
FUNDAMENTAL_DIR = os.path.join(ROOT_DIR, 'data/fundamental/balance_sheet/')


## dow
file_ticker = 'dow_tickers.csv'
file_balance_sheet = 'balance_sheet_dow.csv'
tickers_dow = list()
with open(TICKERS_DIR+file_ticker, newline='') as csvfile:
    ticker_reader = csv.reader(csvfile, delimiter=',')
    for row in ticker_reader:
        tickers_dow.append(row)

balance_sheet_total = pd.DataFrame()
for ticker in tickers_dow[0]:
    balance_sheet = get_balance_sheet(ticker, yearly=True)
    balance_sheet = balance_sheet.T
    balance_sheet = balance_sheet.reset_index()
    balance_sheet['ticker'] = ticker
    balance_sheet_total = balance_sheet_total.append(balance_sheet, ignore_index=True)

balance_sheet_total.to_csv(FUNDAMENTAL_DIR+file_balance_sheet, index=False)

1