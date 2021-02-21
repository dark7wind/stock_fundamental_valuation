import yaml
import MySQLdb as mdb
from definitions import DATABASE_CONFIG_DIR
import pandas as pd
pd.set_option('display.max_columns', None)

def get_input_finance_func(ticker, read_from_sql=True):
    if read_from_sql:
        # load the database configuration
        with open(DATABASE_CONFIG_DIR) as f:
            db_config = yaml.load(f, Loader=yaml.FullLoader)

        db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                         db=db_config['db_name'], use_unicode=True, charset="utf8")

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

        # balance_sheet
        table_name = 'balance_sheet'
        columns_list = ['endDate', 'type', 'shortLongTermDebt', 'longTermDebt', 'cash', 'minorityInterest']
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

    else:
        pass


if __name__ == '__main__':
    ticker = 'TSN'
    get_input_finance_func(ticker)
