import csv
import os
from definitions import ROOT_DIR
from yahoo_fin.stock_info import *
import numpy as np

pd.set_option('display.max_columns', None)

TICKERS_DIR = os.path.join(ROOT_DIR, 'data/tickers/')
FUNDAMENTAL_DIR = os.path.join(ROOT_DIR, 'data/fundamental/analysis_info/')


## dow
file_ticker = 'dow_tickers.csv'
file_analysts_info_total = 'analysis_info_dow.csv'
tickers_dow = list()
with open(TICKERS_DIR+file_ticker, newline='') as csvfile:
    ticker_reader = csv.reader(csvfile, delimiter=',')
    for row in ticker_reader:
        tickers_dow.append(row)

analysts_info_total = pd.DataFrame()
for ticker in tickers_dow[0]:
    analysts_info = get_analysts_info(ticker)

    # revenue estimate
    df_revenue_estimate = analysts_info['Revenue Estimate']
    df_revenue_estimate = df_revenue_estimate.T
    df_revenue_estimate.columns = df_revenue_estimate.iloc[0]
    df_revenue_estimate = df_revenue_estimate[1:]
    df_revenue_estimate = df_revenue_estimate.reset_index()
    ## clean the column name
    df_revenue_estimate.columns = df_revenue_estimate.columns.str.replace(' ', '') # remove the column names
    df_revenue_estimate.columns = df_revenue_estimate.columns.str.replace('.', '') # remove the column names
    df_revenue_estimate = df_revenue_estimate.rename(columns={'SalesGrowth(year/est)':'SalesGrowth'})
    ## only select the yearly estimation
    df_revenue_estimate = df_revenue_estimate[df_revenue_estimate['index'].str.contains('year', case=False)]
    ## determine if it is the current year's estimation
    df_revenue_estimate['CurrentYear'] = df_revenue_estimate.apply(lambda x: 'Current' in x['index'], axis=1)
    ## select the current year
    current_year = df_revenue_estimate[df_revenue_estimate['index'].str.contains('current year', case=False)]\
        ['index'].values[0][-5:-1]
    df_revenue_estimate['Year'] = current_year
    df_revenue_estimate['Ticker'] = ticker
    ## drop the index column
    df_revenue_estimate = df_revenue_estimate.drop(['index'], axis=1)

    analysts_info = analysts_info.T
    analysts_info = analysts_info.reset_index()
    analysts_info['ticker'] = ticker
    analysts_info_total = analysts_info_total.append(analysts_info, ignore_index=True)

analysts_info_total.to_csv(FUNDAMENTAL_DIR+file_analysts_info_total, index=False)

1