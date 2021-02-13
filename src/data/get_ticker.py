import csv
import os
import pandas as pd
from definitions import TICKERS_DIR
from yahoo_fin.stock_info import *




def get_ticker(write_to_local=False):
    # sp500
    sp500_tickers = tickers_sp500()
    if write_to_local:
        file_name = 'sp500_tickers.csv'
        with open(TICKERS_DIR+file_name, mode='w') as ticker_file:
            ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            ticker_writer.writerow(sp500_tickers)
    df_sp500 = pd.DataFrame()
    df_sp500['ticker'] = sp500_tickers
    df_sp500['sp500'] = True

    # dow
    dow_tickers = tickers_dow()
    if write_to_local:
        file_name = 'dow_tickers.csv'
        with open(TICKERS_DIR+file_name, mode='w') as ticker_file:
            ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            ticker_writer.writerow(dow_tickers)
    df_dow = pd.DataFrame()
    df_dow['ticker'] = dow_tickers
    df_dow['dow'] = True

    # # nasdaq
    nasdaq_tickers = tickers_nasdaq()
    if write_to_local:
        file_name = 'nasdaq_tickers.csv'
        with open(TICKERS_DIR+file_name, mode='w') as ticker_file:
            ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            ticker_writer.writerow(nasdaq_tickers)
    df_nasdaq = pd.DataFrame()
    df_nasdaq['ticker'] = nasdaq_tickers


    # # other tickers
    other_tickers = tickers_other()
    if write_to_local:
        file_name = 'other_tickers.csv'
        with open(TICKERS_DIR+file_name, mode='w') as ticker_file:
            ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            ticker_writer.writerow(other_tickers)

    # tickers all
    tickers = list(set().union(sp500_tickers, dow_tickers, nasdaq_tickers, other_tickers))
    # tickers = list(set().union(sp500_tickers, dow_tickers))

    df_tickers = pd.DataFrame()
    df_tickers['ticker'] = tickers
    df_tickers['dow'] = df_tickers['ticker'].apply(lambda x: True if x in dow_tickers else False)
    df_tickers['sp500'] = df_tickers['ticker'].apply(lambda x: True if x in sp500_tickers else False)
    df_tickers['exchange'] = df_tickers['ticker'].apply(lambda x: 'nasdaq' if x in nasdaq_tickers else None)
    df_tickers = df_tickers.loc[df_tickers['ticker'].str.len()>0]
    # write to local
    if write_to_local:
        file_name = 'all_tickers.csv'
        df_tickers.to_csv(TICKERS_DIR+file_name, index=False)

    # check
    print('number of total stocks: {}'.format(len(df_tickers['ticker'])))
    print('number of unique stocks: {}'.format(df_tickers['ticker'].nunique()))
    print('number of stocks in DOW: {}'.format(len(df_tickers.loc[df_tickers['dow']==True])))
    print('number of stocks in SP500: {}'.format(len(df_tickers.loc[df_tickers['sp500']==True])))
    print('number of stocks in NASDAQ: {}'.format(len(df_tickers.loc[df_tickers['exchange']=='nasdaq'])))

    return df_tickers

if __name__ == '__main__':
    write_to_local = False
    get_ticker(write_to_local)
