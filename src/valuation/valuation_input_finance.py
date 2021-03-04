import yaml
import MySQLdb as mdb
from definitions import DATABASE_CONFIG_DIR
import pandas as pd
pd.set_option('display.max_columns', None)

def get_input_finance_func(ticker, read_from_sql=True, read_TTM=False):
    # load the database configuration
    with open(DATABASE_CONFIG_DIR) as f:
        db_config = yaml.load(f, Loader=yaml.FullLoader)

    db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                     db=db_config['db_name'], use_unicode=True, charset="utf8")

    if read_from_sql and not read_TTM:
        # income_statement
        table_name = 'income_statement'
        columns_list = ['endDate', 'type', 'totalRevenue', 'incomeBeforeTax', 'incomeTaxExpense']
        columns = ','.join(columns_list)
        req = """SELECT %s FROM %s WHERE ticker='%s' """ % (columns, table_name, ticker)
        income_statement_cursor = db.cursor()
        income_statement_cursor.execute(req)
        income_statement = income_statement_cursor.fetchall()
        income_statement_cursor.close
        ## create the dataframe
        df_income_statement = pd.DataFrame(income_statement, columns=columns_list)

    elif read_from_sql and read_TTM:
        # income_statement_TTM
        table_name = 'income_statement_TTM'
        columns_list = ['LastUpdatedDate', 'Type', 'TotalRevenue', 'PretaxIncome', 'TaxProvision']
        columns = ','.join(columns_list)
        req = """SELECT %s FROM %s WHERE ticker='%s' """ % (columns, table_name, ticker)
        income_statement_cursor = db.cursor()
        income_statement_cursor.execute(req)
        income_statement = income_statement_cursor.fetchall()
        income_statement_cursor.close
        ## create the dataframe
        df_income_statement = pd.DataFrame(income_statement, columns=columns_list)

    # balance_sheet
    table_name = 'balance_sheet'
    columns_list = ['endDate', 'type', 'shortLongTermDebt', 'longTermDebt', 'cash', 'minorityInterest',
                    'totalStockholderEquity']
    columns = ','.join(columns_list)
    req = """SELECT %s FROM %s WHERE ticker='%s' """ % (columns, table_name, ticker)
    balance_sheet_cursor = db.cursor()
    balance_sheet_cursor.execute(req)
    balance_sheet = balance_sheet_cursor.fetchall()
    balance_sheet_cursor.close
    ## create the dataframe
    df_balance_sheet = pd.DataFrame(balance_sheet, columns=columns_list)

    # stock_statistics
    table_name = 'stock_statistics'
    columns_list = ['createdDate', 'lastUpdatedDate', 'sharesOutstanding']
    columns = ','.join(columns_list)
    req = """SELECT %s FROM %s WHERE ticker='%s' """ % (columns, table_name, ticker)
    stock_statistics_cursor = db.cursor()
    stock_statistics_cursor.execute(req)
    stock_statistics = stock_statistics_cursor.fetchall()
    ## create the dataframe
    df_stock_statistics = pd.DataFrame(stock_statistics, columns=columns_list)

    return df_income_statement, df_balance_sheet, df_stock_statistics

def get_input_price_func(ticker):
    # load the database configuration
    with open(DATABASE_CONFIG_DIR) as f:
        db_config = yaml.load(f, Loader=yaml.FullLoader)

    db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                     db=db_config['db_name'], use_unicode=True, charset="utf8")

    # histoical_price
    table_name = 'historical_price'
    columns_list = ['date', 'ticker', 'close', 'adjclose']
    columns = ','.join(columns_list)
    columns_1 = columns_list[0]
    columns_2 = ','.join(columns_list[1:])
    req = """SELECT %s FROM %s WHERE ticker='%s' and date = (SELECT MAX(%s) FROM %s)""" % (columns, table_name, ticker,
                                                                                          columns_1, table_name)
    # SELECT * FROM historical_price WHERE ticker = 'TSN' and date = (SELECT MAX(date) FROM historical_price);

    historical_price_cursor = db.cursor()
    historical_price_cursor.execute(req)
    historical_price = historical_price_cursor.fetchall()
    historical_price_cursor.close
    ## create the dataframe
    df_historical_price = pd.DataFrame(historical_price, columns=columns_list)
    return df_historical_price

def get_analysis_estimate_revenue(ticker):
    # load the database configuration
    with open(DATABASE_CONFIG_DIR) as f:
        db_config = yaml.load(f, Loader=yaml.FullLoader)

    db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                     db=db_config['db_name'], use_unicode=True, charset="utf8")

    # analysis revenue estimation
    table_name = 'analysis_info_revenue'
    columns_list = ['LastUpdatedDate', 'Ticker', 'Year', 'SalesGrowth', 'CurrentYearFlag']
    columns = ','.join(columns_list)
    columns_1 = columns_list[0]
    req = """SELECT %s FROM %s WHERE ticker='%s' and %s = (SELECT MAX(%s) FROM %s)""" % (columns, table_name, ticker,
                                                                                         columns_1, columns_1, table_name)
    reveune_growth_cursor = db.cursor()
    reveune_growth_cursor.execute(req)
    revenue_growth = reveune_growth_cursor.fetchall()
    reveune_growth_cursor.close

    r_gr_next = revenue_growth[0][-2]
    r_gr_next = float(r_gr_next.strip('%')) / 100

    r_gr_high = revenue_growth[1][-2]
    r_gr_high = float(r_gr_high.strip('%')) / 100

    return r_gr_next, r_gr_high

if __name__ == '__main__':
    ticker = 'KR'
    get_input_finance_func(ticker)
    get_input_price_func(ticker)
    get_analysis_estimate_revenue(ticker)