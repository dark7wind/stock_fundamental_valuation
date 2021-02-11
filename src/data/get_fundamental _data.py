import csv
import os
from definitions import ROOT_DIR
from yahoo_fin.stock_info import *

TICKERS_DIR = os.path.join(ROOT_DIR, 'data/tickers/')
FUNDAMENTAL_DIR = os.path.join(ROOT_DIR, 'data/fundamental/')

ticker = 'tsn'

# income statement
## dow
file_ticker = 'dow_tickers.csv'
file_income_statement = 'dow_income_statement.csv'
tickers_dow = list()
with open(TICKERS_DIR+file_ticker, newline='') as csvfile:
    ticker_reader = csv.reader(csvfile, delimiter=',')
    for row in ticker_reader:
        tickers_dow.append(row)

income_statement_total = pd.DataFrame()
for ticker in tickers_dow[0]:
    income_statement = get_income_statement(ticker, yearly=True)
    income_statement = income_statement.T
    income_statement = income_statement.reset_index()
    income_statement['ticker'] = ticker
    income_statement_total = income_statement_total.append(income_statement, ignore_index=True)

income_statement_total.to_csv(FUNDAMENTAL_DIR+file_income_statement, index=False)

1