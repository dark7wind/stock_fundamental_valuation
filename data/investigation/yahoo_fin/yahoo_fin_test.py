# import yahoo_fin
from yahoo_fin.stock_info import *

ticker = tickers_sp500()
cash_flow = get_cash_flow('nflx')
income_statement = get_income_statement('nflx')
1