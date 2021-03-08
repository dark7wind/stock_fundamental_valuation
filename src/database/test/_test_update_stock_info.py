import pandas as pd
pd.set_option('display.max_columns', None)

from definitions import PROFILE_DIR

file_name = '20210308_indname.xls'

df_info = pd.read_excel(PROFILE_DIR+file_name)
df_exchange_ticker = df_info['Exchange:Ticker'].str.split(':', expand=True)
df_exchange_ticker.columns = ['Exchange', 'Ticker']
df_info = pd.concat([df_info, df_exchange_ticker], axis=1)
df_info = df_info.drop(['Exchange:Ticker'], axis=1)

## replace NasdaqGS, NasdaqGM, NasdaqCM --> Nasdaq
df_info['Exchange'] = df_info['Exchange'].str.replace(r'Nasdaq[A-Z]*', 'NASDAQ', regex=True)

## remove the space in the column name
df_info.columns = df_info.columns.str.replace(' ', '')

df_inf_usa = df_info.loc[(df_info['Exchange']=='NYSE') | (df_info['Exchange']=='NASDAQ')]

1