import csv
import os
from definitions import ROOT_DIR
from yahoo_fin.stock_info import *

TICKERS_DIR = os.path.join(ROOT_DIR, 'data/tickers/')
FUNDAMENTAL_DIR = os.path.join(ROOT_DIR, 'data/fundamental/cash_flow/')


## dow
file_ticker = 'dow_tickers.csv'
file_cash_flow = 'cash_flow_dow.csv'
tickers_dow = list()
with open(TICKERS_DIR+file_ticker, newline='') as csvfile:
    ticker_reader = csv.reader(csvfile, delimiter=',')
    for row in ticker_reader:
        tickers_dow.append(row)

cash_flow_total = pd.DataFrame()
for ticker in tickers_dow[0]:
    cash_flow = get_cash_flow(ticker)
    cash_flow = cash_flow.T
    cash_flow = cash_flow.reset_index()
    cash_flow['ticker'] = ticker
    cash_flow_total = cash_flow_total.append(cash_flow, ignore_index=True)

cash_flow_total.to_csv(FUNDAMENTAL_DIR+file_cash_flow, index=False)

1