from yahoo_fin.stock_info import *

def get_balance_sheet_single_stock(stock_id, ticker):
    try:
        df_balance_sheet = get_balance_sheet(ticker, yearly=True)
        print('get the data')
        df_balance_sheet = df_balance_sheet.T
        df_balance_sheet = df_balance_sheet.reset_index()
        df_balance_sheet['stockId'] = stock_id
        df_balance_sheet['ticker'] = ticker
        return df_balance_sheet
    except Exception:
        print('no data')
        return None