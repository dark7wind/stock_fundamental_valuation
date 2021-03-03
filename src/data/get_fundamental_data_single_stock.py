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

def get_analysis_info_revenue_single_stock(stock_id, ticker):
    try:
        analysts_info = get_analysts_info(ticker)
        print('get the analysis info revenue data')
        # revenue estimate
        df_revenue_estimate = analysts_info['Revenue Estimate']
        df_revenue_estimate = df_revenue_estimate.T
        df_revenue_estimate.columns = df_revenue_estimate.iloc[0]
        df_revenue_estimate = df_revenue_estimate[1:]
        df_revenue_estimate = df_revenue_estimate.reset_index()
        ## clean the column name
        df_revenue_estimate.columns = df_revenue_estimate.columns.str.replace(' ', '')  # remove the space
        df_revenue_estimate.columns = df_revenue_estimate.columns.str.replace('.', '')  # remove the .
        df_revenue_estimate = df_revenue_estimate.rename(columns={'SalesGrowth(year/est)': 'SalesGrowth'})
        ## only select the yearly estimation
        df_revenue_estimate = df_revenue_estimate[df_revenue_estimate['index'].str.contains('year', case=False)]
        ## determine if it is the current year's estimation
        df_revenue_estimate['CurrentYearFlag'] = df_revenue_estimate.apply(lambda x: 'Current' in x['index'], axis=1)
        ## select the current year
        current_year = df_revenue_estimate[df_revenue_estimate['index'].str.contains('current year', case=False)] \
                           ['index'].values[0][-5:-1]
        df_revenue_estimate['Year'] = current_year
        df_revenue_estimate['Ticker'] = ticker
        df_revenue_estimate['stockId'] = stock_id
        ## drop the index column
        df_revenue_estimate = df_revenue_estimate.drop(['index'], axis=1)
        return df_revenue_estimate
    except Exception:
        print('no data')
        return None