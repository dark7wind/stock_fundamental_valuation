import yfinance as yf
import MySQLdb as mdb
import os
import yaml
import datetime
import pandas as pd
from definitions import DATABASE_CONFIG_DIR, PROFILE_DIR
import time

def download_profile():
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_profile = 'profile_sp500.csv'

    if os.path.exists(PROFILE_DIR+file_date+'_'+file_profile):
        df_file_profile_total = pd.read_csv(PROFILE_DIR+file_date+'_'+file_profile)
        # print(df_income_statement_total.columns)
        return df_file_profile_total

    else:
        # connect the database
        with open(DATABASE_CONFIG_DIR) as f:
            db_config = yaml.load(f, Loader=yaml.FullLoader)

        db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                         db=db_config['db_name'], use_unicode=True, charset="utf8")

        # select stockId and ticker from table stock_info
        table_name = 'stock_info'
        columns = ','.join(['stockId', 'ticker'])
        req = """SELECT %s FROM %s WHERE SP500=TRUE""" % (columns, table_name)  # first try SP500 stocks
        get_ticker_cursor = db.cursor()
        get_ticker_cursor.execute(req)
        stockId_ticker = get_ticker_cursor.fetchall()
        get_ticker_cursor.close()

        # get the profile data
        df_profile = pd.DataFrame()
        sector_list = list()
        industry_list = list()
        ticker_list = list()
        stock_id_list = list()
        for stock_id, ticker in stockId_ticker:
            try:
                print(f'stockId: {stock_id}, ticker: {ticker}')
                tickerdata = yf.Ticker(ticker)
                ticker_sector = tickerdata.info['sector']
                ticker_industry = tickerdata.info['industry']
                sector_list.append(ticker_sector)
                industry_list.append(ticker_industry)
                ticker_list.append(ticker)
                stock_id_list.append(stock_id)
                time.sleep(1)
            except:
                print(f'stockId: {stock_id}, ticker: {ticker} has error')

        df_profile = pd.DataFrame(list(zip(stock_id_list, ticker_list, sector_list, industry_list)),
                                  columns=['StockId', 'Ticker', 'SectorYahoo', 'IndustryYahoo'])

        # write to csv
        df_profile.to_csv(PROFILE_DIR + file_date + '_' + file_profile, index=False)


if __name__ == '__main__':
    download_profile()
