from yahoo_fin.stock_info import *

def get_cash_flow_single_stock(stock_id, ticker):
    try:
        df_cash_flow = get_cash_flow(ticker, yearly=True)
        print('get the data')
        df_cash_flow = df_cash_flow.T
        df_cash_flow = df_cash_flow.reset_index()
        df_cash_flow['stockId'] = stock_id
        df_cash_flow['ticker'] = ticker
        return df_cash_flow
    except Exception:
        print('no data')
        return None
