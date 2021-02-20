from yahoo_fin.stock_info import *

def get_income_statement_single_stock_yearly(stock_id, ticker):
    try:
        df_income_statement = get_income_statement(ticker, yearly=True)
        print('get the yearly data')
        df_income_statement = df_income_statement.T
        df_income_statement = df_income_statement.reset_index()
        df_income_statement['stockId'] = stock_id
        df_income_statement['ticker'] = ticker
        df_income_statement['type'] = 'yearly'
        return df_income_statement
    except Exception:
        print('no data')
        return None


def get_income_statement_single_stock_quarterly(stock_id, ticker):
    try:
        df_income_statement = get_income_statement(ticker, yearly=False)
        print('get the quarterly data')
        df_income_statement = df_income_statement.T
        df_income_statement = df_income_statement.reset_index()
        df_income_statement['stockId'] = stock_id
        df_income_statement['ticker'] = ticker
        df_income_statement['type'] = 'quarterly'
        return df_income_statement
    except Exception:
        print('no data')
        return None

def get_balance_sheet_single_stock_yearly(stock_id, ticker):
    try:
        df_balance_sheet = get_balance_sheet(ticker, yearly=True)
        print('get the yearly data')
        df_balance_sheet = df_balance_sheet.T
        df_balance_sheet = df_balance_sheet.reset_index()
        df_balance_sheet['stockId'] = stock_id
        df_balance_sheet['ticker'] = ticker
        df_balance_sheet['type'] = 'yearly'
        return df_balance_sheet
    except Exception:
        print('no data')
        return None

def get_balance_sheet_single_stock_quarterly(stock_id, ticker):
    try:
        df_balance_sheet = get_balance_sheet(ticker, yearly=False)
        print('get the quarterly data')
        df_balance_sheet = df_balance_sheet.T
        df_balance_sheet = df_balance_sheet.reset_index()
        df_balance_sheet['stockId'] = stock_id
        df_balance_sheet['ticker'] = ticker
        df_balance_sheet['type'] = 'quarterly'
        return df_balance_sheet
    except Exception:
        print('no data')
        return None

def get_cash_flow_single_stock_yearly(stock_id, ticker):
    try:
        df_cash_flow = get_cash_flow(ticker, yearly=True)
        print('get the yearly data')
        df_cash_flow = df_cash_flow.T
        df_cash_flow = df_cash_flow.reset_index()
        df_cash_flow['stockId'] = stock_id
        df_cash_flow['ticker'] = ticker
        df_cash_flow['type'] = 'yearly'
        return df_cash_flow
    except Exception:
        print('no data')
        return None

def get_cash_flow_single_stock_quarterly(stock_id, ticker):
    try:
        df_cash_flow = get_cash_flow(ticker, yearly=False)
        print('get the quarterly data')
        df_cash_flow = df_cash_flow.T
        df_cash_flow = df_cash_flow.reset_index()
        df_cash_flow['stockId'] = stock_id
        df_cash_flow['ticker'] = ticker
        df_cash_flow['type'] = 'quarterly'
        return df_cash_flow
    except Exception:
        print('no data')
        return None

def get_stock_statistics_single_stock(stock_id, ticker):
    try:
        statistics = get_stats(ticker)
        print('get the statistics data')
        statistics = statistics.set_index(['Attribute'])
        statistics = statistics.T
        statistics = statistics.reset_index()
        statistics.drop(columns=['index'], inplace=True)
        statistics['ticker'] = ticker
        statistics['stockId'] = stock_id
        return statistics
    except Exception:
        print('no data')
        return None
