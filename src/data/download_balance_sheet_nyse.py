import MySQLdb as mdb
import os
import yaml
import datetime
from src.data.get_fundamental_data_single_stock import get_balance_sheet_single_stock_yearly, \
    get_balance_sheet_single_stock_quarterly
from yahoo_fin.stock_info import *
from definitions import DATABASE_CONFIG_DIR, BALANCE_SHEET_DIR

def download_balance_sheet():
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_balance_sheet = 'balance_sheet_nyse.csv'
    1
    if os.path.exists(BALANCE_SHEET_DIR+file_date+'_'+file_balance_sheet):
        df_balance_sheet_total = pd.read_csv(BALANCE_SHEET_DIR+file_date+'_'+file_balance_sheet)
        # print(df_income_statement_total.columns)
        return df_balance_sheet_total

    else:
        # connect the database
        with open(DATABASE_CONFIG_DIR) as f:
            db_config = yaml.load(f, Loader=yaml.FullLoader)

        db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                         db=db_config['db_name'], use_unicode=True, charset="utf8")

        # select stockId and ticker from table stock_info
        table_name = 'stock_info'
        columns = ','.join(['stockId', 'ticker'])
        req = """SELECT %s FROM %s WHERE exchange='NYSE'""" % (columns, table_name)
        get_ticker_cursor = db.cursor()
        get_ticker_cursor.execute(req)
        stockId_ticker = get_ticker_cursor.fetchall()
        get_ticker_cursor.close()

        # get the balance_sheet data from Yahoo
        df_balance_sheet_yearly_total = pd.DataFrame()
        df_balance_sheet_quarterly_total = pd.DataFrame()
        for stock_id, ticker in stockId_ticker:
            print(f'stockId: {stock_id}, ticker: {ticker}')
            df_balance_sheet_yearly = get_balance_sheet_single_stock_yearly(stock_id, ticker)
            df_balance_sheet_yearly_total = df_balance_sheet_yearly_total.append(df_balance_sheet_yearly,
                                                                                 ignore_index=True)
            df_balance_sheet_quarterly = get_balance_sheet_single_stock_quarterly(stock_id, ticker)
            df_balance_sheet_quarterly_total = df_balance_sheet_quarterly_total.append(df_balance_sheet_quarterly,
                                                                                 ignore_index=True)

        # concat two dataframes
        df_balance_sheet_total = pd.concat([df_balance_sheet_yearly_total, df_balance_sheet_quarterly_total])

        # write to csv
        df_balance_sheet_total.to_csv(BALANCE_SHEET_DIR+file_date+'_'+file_balance_sheet, index=False)
        # print(df_income_statement_total.columns)
        return df_balance_sheet_total

if __name__ == '__main__':
    download_balance_sheet()
