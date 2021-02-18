from yahoo_fin.stock_info import *

def get_income_statement_single_stock(stock_id, ticker):
    try:
        df_income_statement = get_income_statement(ticker, yearly=True)
        print('get the yearly data')
        df_income_statement = df_income_statement.T
        df_income_statement = df_income_statement.reset_index()
        df_income_statement['stockId'] = stock_id
        df_income_statement['ticker'] = ticker
        return df_income_statement
    except Exception:
        print('no data')
        return None