import MySQLdb as mdb
import pandas as pd
pd.set_option('display.max_columns', None)
import datetime
import numpy as np
import yaml
from definitions import DATABASE_CONFIG_DIR, TICKERS_DIR, PROFILE_DIR
from src.data.download_ticker import download_ticker


# load the database configuration
with open(DATABASE_CONFIG_DIR) as f:
    db_config = yaml.load(f, Loader=yaml.FullLoader)


db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                 db=db_config['db_name'], use_unicode=True, charset="utf8")

df = pd.DataFrame()
def insert_stock_info_data_into_db():
    # create the time now (utc time)
    now = datetime.datetime.utcnow()

    # get tickers
    df_ticker = download_ticker()
    ## CreatedDate and lastUpdatedDate
    df_ticker['CreatedDate'] = now
    df_ticker['LastUpdatedDate'] = now
    # drop the exchange column
    df_ticker = df_ticker.drop(['exchange'], axis=1)
    # capitalize the column name
    new_columns = list()
    for column in df_ticker.columns:
        new_column = column[:1].upper() + column[1:]
        new_columns.append(new_column)
    df_ticker.columns = new_columns

    # usa info industry, exchange, company name
    file_name = '20210308_indname.xls'
    df_info = pd.read_excel(PROFILE_DIR + file_name)
    df_exchange_ticker = df_info['Exchange:Ticker'].str.split(':', expand=True)
    df_exchange_ticker.columns = ['Exchange', 'Ticker']
    df_info = pd.concat([df_info, df_exchange_ticker], axis=1)
    df_info = df_info.drop(['Exchange:Ticker'], axis=1)
    # remove the character ' in CompanyName
    ## replace NasdaqGS, NasdaqGM, NasdaqCM --> Nasdaq
    df_info['Exchange'] = df_info['Exchange'].str.replace(r'Nasdaq[A-Z]*', 'NASDAQ', regex=True)
    ## remove the space in the column name
    df_info.columns = df_info.columns.str.replace(' ', '')
    df_info['CompanyName'] = df_info['CompanyName'].replace({'\'': ' '}, regex=True)
    ## get usa data
    df_inf_usa = df_info.loc[(df_info['Exchange'] == 'NYSE') | (df_info['Exchange'] == 'NASDAQ')]
    ## drop the duplicates
    df_inf_usa = df_inf_usa.drop_duplicates()

    ## merge with df_inf_usa
    df = df_ticker.merge(df_inf_usa, left_on='Ticker', right_on='Ticker', how='left')
    # covert nan to empty
    df = df.replace(np.nan, 'empty')

    # create req strings
    table_name = 'stock_info'
    columns = ','.join(df.columns.values)
    values = ("%s, " * len(df.columns))[:-2]

    mysql_cursor = db.cursor()
    for i in range(len(df.index)):
        print('update ticker: %s' % df.loc[i,'Ticker'])
        req = """UPDATE %s SET Dow=%s, Sp500=%s, CreatedDate='%s', LastUpdatedDate='%s', CompanyName='%s', \
        IndustryGroup='%s', Country='%s', BroadGroup='%s', SubGroup='%s', Exchange='%s' WHERE Ticker='%s' """ % \
              (table_name, df.loc[i,'Dow'], df.loc[i,'Sp500'], df.loc[i,'CreatedDate'], df.loc[i,'LastUpdatedDate'], \
               df.loc[i,'CompanyName'], df.loc[i,'IndustryGroup'], df.loc[i,'Country'], df.loc[i,'BroadGroup'], \
               df.loc[i,'SubGroup'], df.loc[i, 'Exchange'], df.loc[i,'Ticker'])
        mysql_cursor.execute(req)
        db.commit()

    mysql_cursor.close()



if __name__ == '__main__':
    insert_stock_info_data_into_db()
