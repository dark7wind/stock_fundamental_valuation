import MySQLdb as mdb
import os
import yaml
import datetime
import numpy as np
from definitions import DATABASE_CONFIG_DIR, ANALYSIS_INFO_DIR
from src.data.get_fundamental_data_single_stock import get_analysis_info_revenue_single_stock
from yahoo_fin.stock_info import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.set_option('display.max_columns', None)


def download_analysis_info():
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_analysis_info_revenue = 'analysis_info_revenue_nyse.csv'

    if os.path.exists(ANALYSIS_INFO_DIR+file_date+'_'+file_analysis_info_revenue):
        df_analysis_info_revenue_total = pd.read_csv(ANALYSIS_INFO_DIR+file_date+'_'+file_analysis_info_revenue)
        # print(df_income_statement_total.columns)
        return df_analysis_info_revenue_total
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

        # get the analysis info data from Yahoo
        df_analysis_info_revenue_total = pd.DataFrame()
        for stock_id, ticker in stockId_ticker:
            print(f'stockId: {stock_id}, ticker: {ticker}')
            df_revenue_estimate = get_analysis_info_revenue_single_stock(stock_id, ticker)
            df_analysis_info_revenue_total = df_analysis_info_revenue_total.append(df_revenue_estimate, \
                                                                                   ignore_index=True)

        # write to csv
        df_analysis_info_revenue_total.to_csv(ANALYSIS_INFO_DIR + file_date + '_' + file_analysis_info_revenue, \
                                              index=False)
        # print(df_income_statement_total.columns)
        return df_analysis_info_revenue_total





if __name__ == '__main__':
    download_analysis_info()