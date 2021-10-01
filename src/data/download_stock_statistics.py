import os
import datetime
import yaml
import pandas as pd
pd.set_option('display.max_columns', None)
import MySQLdb as mdb
from definitions import DATABASE_CONFIG_DIR, STATISTICS_DIR
from src.data.get_fundamental_data_single_stock import get_stock_statistics_single_stock

def download_stock_statistics():
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_statistics = 'statistics.csv'

    if os.path.exists(STATISTICS_DIR + file_date + '_' + file_statistics):
        df_statistics_total= pd.read_csv(STATISTICS_DIR+file_date+'_'+file_statistics)
        return df_statistics_total
    else:
        # connect the database
        with open(DATABASE_CONFIG_DIR) as f:
            db_config = yaml.load(f, Loader=yaml.FullLoader)

        db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                         db=db_config['db_name'], use_unicode=True, charset="utf8")

        # select stockId and ticker from table stock_info
        table_name = 'stock_info'
        columns = ','.join(['stockId', 'ticker'])
        req = """SELECT %s FROM %s WHERE sp500=TRUE""" % (columns, table_name)
        get_ticker_cursor = db.cursor()
        get_ticker_cursor.execute(req)
        stockId_ticker = get_ticker_cursor.fetchall()
        get_ticker_cursor.close()

        # get the income_statement data from Yahoo
        df_statistics_total = pd.DataFrame()
        for stock_id, ticker in stockId_ticker:
            print(f'stockId: {stock_id}, ticker: {ticker}')
            df_statistics = get_stock_statistics_single_stock(stock_id, ticker)
            df_statistics_total = df_statistics_total.append(df_statistics, ignore_index=True)

        # write to csv
        df_statistics_total.to_csv(STATISTICS_DIR+file_date+'_'+file_statistics, index=False)
        return df_statistics_total


if __name__ == '__main__':
    download_stock_statistics()

#
# TICKERS_DIR = os.path.join(ROOT_DIR, 'data/tickers/')
# FUNDAMENTAL_DIR = os.path.join(ROOT_DIR, 'data/fundamental/statistics/')
#
# ## dow
# file_ticker = 'dow_tickers.csv'
# file_statistics = 'statistics_dow.csv'
# tickers_dow = list()
# with open(TICKERS_DIR+file_ticker, newline='') as csvfile:
#     ticker_reader = csv.reader(csvfile, delimiter=',')
#     for row in ticker_reader:
#         tickers_dow.append(row)
#
# statistics_total = pd.DataFrame()
# for ticker in tickers_dow[0]:
#     statistics = get_stats(ticker)
#     statistics = statistics.set_index(['Attribute'])
#     statistics = statistics.T
#     statistics = statistics.reset_index()
#     statistics.drop(columns=['index'], inplace=True)
#     statistics['ticker'] = ticker
#     statistics_total = statistics_total.append(statistics, ignore_index=True)
#
# statistics_total.to_csv(FUNDAMENTAL_DIR+file_statistics, index=False)
#
