import MySQLdb as mdb
import os
import yaml
import datetime
from src.data.get_fundamental_data_single_stock import get_cash_flow_single_stock_yearly, \
    get_cash_flow_single_stock_quarterly
from yahoo_fin.stock_info import *
from definitions import DATABASE_CONFIG_DIR, CASH_FLOW_DIR

def download_cahs_flow():
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_cash_flow = 'cash_flow_nyse.csv'

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
        req = """SELECT %s FROM %s WHERE exchange='nyse'""" % (columns, table_name) # first try SP500 stocks
        get_ticker_cursor = db.cursor()
        get_ticker_cursor.execute(req)
        stockId_ticker = get_ticker_cursor.fetchall()
        get_ticker_cursor.close()

        # get the cash_flow data from Yahoo
        df_cash_flow_yearly_total = pd.DataFrame()
        df_cash_flow_quarterly_total = pd.DataFrame()
        for stock_id, ticker in stockId_ticker:
            print(f'stockId: {stock_id}, ticker: {ticker}')
            df_cash_flow_yearly = get_cash_flow_single_stock_yearly(stock_id, ticker)
            df_cash_flow_yearly_total = df_cash_flow_yearly_total.append(df_cash_flow_yearly, ignore_index=True)
            df_cash_flow_quarterly = get_cash_flow_single_stock_quarterly(stock_id, ticker)
            df_cash_flow_quarterly_total = df_cash_flow_quarterly_total.append(df_cash_flow_quarterly, ignore_index=True)

        # concat two dataframes
        df_cash_flow_total = pd.concat([df_cash_flow_yearly_total, df_cash_flow_quarterly_total])

        # write to csv
        df_cash_flow_total.to_csv(CASH_FLOW_DIR + file_date + '_' + file_cash_flow, index=False)
        # print(df_income_statement_total.columns)
        return df_cash_flow_total

    1

if __name__ == '__main__':
    download_cahs_flow()

