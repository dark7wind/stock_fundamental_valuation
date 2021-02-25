from src.data.scraping_fundamental_function import *
import MySQLdb as mdb
import os
import yaml
import datetime
from definitions import DATABASE_CONFIG_DIR, INCOME_STATEMENT_DIR
import time


def download_income_statement_TTM():
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_income_statement = 'income_statement_TTM.csv'

    if os.path.exists(INCOME_STATEMENT_DIR+file_date+'_'+file_income_statement):
        df_income_statement_total = pd.read_csv(INCOME_STATEMENT_DIR+file_date+'_'+file_income_statement)
        # print(df_income_statement_total.columns)
        return df_income_statement_total
    else:
        # connect the database
        with open(DATABASE_CONFIG_DIR) as f:
            db_config = yaml.load(f, Loader=yaml.FullLoader)

        db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                         db=db_config['db_name'], use_unicode=True, charset="utf8")

        # select stockId and ticker from table stock_info
        table_name = 'stock_info'
        columns = ','.join(['stockId', 'ticker'])
        req = """SELECT %s FROM %s WHERE sp500=TRUE """ % (columns, table_name)
        get_ticker_cursor = db.cursor()
        get_ticker_cursor.execute(req)
        stockId_ticker = get_ticker_cursor.fetchall()
        get_ticker_cursor.close()

        # get the income_statement data (self scraping from Yahoo)
        df_income_statement_total = pd.DataFrame()
        for stock_id, ticker in stockId_ticker:
            print(f'stockId: {stock_id}, ticker: {ticker}')
            url_income_statement = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
            df_income_statement = scrape_table(url_income_statement)
            if not df_income_statement is None:
                df_income_statement = df_income_statement.loc[df_income_statement['Date'] == 'ttm']
                df_income_statement['Ticker'] = ticker
                df_income_statement['StockId'] = stock_id
                df_income_statement_total = df_income_statement_total.append(df_income_statement, ignore_index=True)
            time.sleep(3)
        # concat two dataframes
        df_income_statement_total.columns = df_income_statement_total.columns.str.replace(' ', '')

        # write to csv
        df_income_statement_total.to_csv(INCOME_STATEMENT_DIR + file_date + '_' + file_income_statement, index=False)
        # print(df_income_statement_total.columns)
        return df_income_statement_total


if __name__ == '__main__':
    download_income_statement_TTM()

# url_balance_sheet = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
# df_balance_sheet = scrape_table(url_balance_sheet)
#
# url_cash_flow = f'https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}'
# df_cash_flow = scrape_table(url_cash_flow)
1








#rename_list = {'Date':'endDate', 'Total Revenue':'totalRevenue', 'Cost of Revenue':'costOfRevenue',
#                'Gross Profit':'grossProfit', 'Operating Expense':'totalOperatingExpenses',
#                'Operating Income': 'operatingIncome', 'Net Non Operating Interest Income Expense':'??',
#                'Other Income Expense': '??', 'Pretax Income': 'incomeBeforeTax', 'Tax Provision': 'incomeTaxExpense',
#                'Net Income Common Stockholders':'netIncomeApplicableToCommonShares',
#                'Diluted NI Available to Com Stockholders':'??', 'Basic EPS':'??', 'Diluted EPS':'??',
#                'Basic Average Shares':'??', 'Diluted Average Shares':'??',
#                'Total Operating Income as Reported':'??', 'Total Expenses':'??',
#                'Net Income from Continuing & Discontinued Operation':'??', 'Normalized Income':'??',
#                'Interest Income': '??', 'Interest Expense':'interestExpense', 'Net Interest Income':'??',
#                'EBIT':'??', 'Reconciled Cost of Revenue':'??', 'Reconciled Depreciation':'??',
#                'Reconciled Depreciation':'??',
#                'Net Income from Continuing Operation Net Minority Interest':'minorityInterest',
#                'Normalized EBITDA':'??', 'Tax Rate for Calcs':'??', 'Tax Effect of Unusual Items':'??'}