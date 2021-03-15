import MySQLdb as mdb
import os
import yaml
import datetime
from yahoo_fin.stock_info import *
from definitions import DATABASE_CONFIG_DIR, HISTORICAL_PRICE_DIR
import pandas as pd
pd.set_option('display.max_columns', None)

def download_historical_price():
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_income_statement = 'historical_price_sp500.csv'

    if os.path.exists(HISTORICAL_PRICE_DIR + file_date + '_' + file_income_statement):
        df_historical_price_total = pd.read_csv(HISTORICAL_PRICE_DIR + file_date + '_' + file_income_statement)
        # print(df_historical_price_total.columns)
        return df_historical_price_total
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
        tot_num = len(stockId_ticker)

        # get the income_statement data from Yahoo
        df_historical_price_total = pd.DataFrame()
        n = 0
        for stock_id, ticker in stockId_ticker:
            try:
                n += 1
                progress = round(n / tot_num * 100, 2)
                print(f'stockId: {stock_id}, ticker: {ticker}, progress: {progress} %')
                df_historical_price = get_data(ticker)#, start_date='01/01/1999')
                df_historical_price = df_historical_price.reset_index()
                df_historical_price['stockId'] = stock_id
                df_historical_price = df_historical_price.rename(columns={'index': 'date'})
                df_historical_price_total = df_historical_price_total.append(df_historical_price, ignore_index=True)
            except:
                print(f'Error: cannot get the price data of {ticker}')
        # write to csv
        df_historical_price_total.to_csv(HISTORICAL_PRICE_DIR + file_date + '_' + file_income_statement, index=False)
        return df_historical_price_total

def download_updated_price():
    # extract the latest date
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_income_statement = 'updated_price_sp500.csv'
    if os.path.exists(HISTORICAL_PRICE_DIR + file_date + '_' + file_income_statement):
        df_updated_price_total = pd.read_csv(HISTORICAL_PRICE_DIR + file_date + '_' + file_income_statement)
        # print(df_historical_price_total.columns)
        return df_updated_price_total
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
        tot_num = len(stockId_ticker)

        # extract the latest date
        table_name = 'historical_price'
        columns_list = ['date']
        columns = ','.join(columns_list)
        df_updated_price_total = pd.DataFrame()
        get_latest_date_cursor = db.cursor()
        n = 0
        for stock_id, ticker in stockId_ticker:
            try:
                n += 1
                progress = round(n / tot_num * 100, 2)
                print(f'stockId: {stock_id}, ticker: {ticker}, progress: {progress} %')
                req = """SELECT MAX(%s) FROM %s WHERE ticker = '%s'""" % (columns, table_name, ticker)
                get_latest_date_cursor.execute(req)
                latest_date = get_latest_date_cursor.fetchall()
                latest_date = latest_date[0][0]
                latest_date = datetime.datetime.strptime(latest_date, '%Y-%m-%d')
                start_date = latest_date + datetime.timedelta(days=1)
                start_date = start_date.strftime('%Y-%m-%d')
                df_updated_price = get_data(ticker, start_date=start_date)
                df_updated_price = df_updated_price.reset_index()
                df_updated_price = df_updated_price.drop_duplicates(subset=['index', 'ticker'], keep='first')
                df_updated_price['stockId'] = stock_id
                df_updated_price = df_updated_price.rename(columns={'index': 'date'})
                df_updated_price_total = df_updated_price_total.append(df_updated_price, ignore_index=True)
            except:
                print(f'Error: cannot get the price data of {ticker}')

        get_latest_date_cursor.close()

        # write to csv
        df_updated_price_total.to_csv(HISTORICAL_PRICE_DIR + file_date + '_' + file_income_statement, index=False)
        return df_updated_price_total


if __name__ == '__main__':
    # download_historical_price()
    download_updated_price()