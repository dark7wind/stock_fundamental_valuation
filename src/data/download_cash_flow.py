import MySQLdb as mdb
import os
import yaml
import datetime
from src.data.get_cash_flow_single_stock import get_cash_flow_single_stock
from yahoo_fin.stock_info import *
from definitions import DATABASE_CONFIG_DIR, CASH_FLOW_DIR

def download_cahs_flow():
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_cash_flow = 'cash_flow_sp500.csv'

    if os.path.exists(CASH_FLOW_DIR+file_date+'_'+file_cash_flow):
        df_cash_flow_total = pd.read_csv(CASH_FLOW_DIR+file_date+'_'+file_cash_flow)
        # print(df_income_statement_total.columns)
        return df_cash_flow_total

    else:
        # connect the database
        with open(DATABASE_CONFIG_DIR) as f:
            db_config = yaml.load(f, Loader=yaml.FullLoader)

        db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                         db=db_config['db_name'], use_unicode=True, charset="utf8")

        # select stockId and ticker from table stock_info
        table_name = 'stock_info'
        columns = ','.join(['stockId', 'ticker'])
        req = """SELECT %s FROM %s WHERE SP500=TRUE""" % (columns, table_name) # first try SP500 stocks
        get_ticker_cursor = db.cursor()
        get_ticker_cursor.execute(req)
        stockId_ticker = get_ticker_cursor.fetchall()
        get_ticker_cursor.close()

        # get the balance_sheet data from Yahoo
        df_cash_flow_total = pd.DataFrame()
        for stock_id, ticker in stockId_ticker:
            print(f'stockId: {stock_id}, ticker: {ticker}')
            df_cash_flow = get_cash_flow_single_stock(stock_id, ticker)
            df_cash_flow_total = df_cash_flow_total.append(df_cash_flow, ignore_index=True)

        # write to csv
        df_cash_flow_total.to_csv(CASH_FLOW_DIR + file_date + '_' + file_cash_flow, index=False)
        # print(df_income_statement_total.columns)
        return df_cash_flow_total

    1

if __name__ == '__main__':
    download_cahs_flow()

