import pandas as pd
import numpy as np
import datetime
import yaml
import MySQLdb as mdb
from definitions import INDUSTRY_DIR, DATABASE_CONFIG_DIR
pd.set_option('display.max_columns', None)


def insert_industry_data_into_db(file_name):
    # load the database configuration
    with open(DATABASE_CONFIG_DIR) as f:
        db_config = yaml.load(f, Loader=yaml.FullLoader)

    db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                     db=db_config['db_name'], use_unicode=True, charset="utf8")

    # load the file
    df = pd.read_csv(INDUSTRY_DIR+file_name)
    # clean the column names
    df.columns = df.columns.str.replace(' ', '')
    df.columns = df.columns.str.replace('-', '')
    df.columns = df.columns.str.replace("[/,@,&,%,-,(,)]", "", regex=True)

    # createDate and lastUpdatedDate
    now = datetime.datetime.utcnow()
    df['CreatedDate'] = now
    df['LastUpdatedDate'] = now

    # Date
    date = file_name[0:8]
    date = datetime.datetime.strptime(date, '%Y%m%d')
    df['Date'] = date

    # region
    if 'Global' in file_name:
        df['Region'] = 'Global'
    elif 'US' in file_name:
        df['Region'] = 'US'



    # covert nan to 0 for numerical column, empty for non-numerical column
    ## numbercial columns
    df_num = df.select_dtypes(include=[np.number])
    num_columns = df_num.columns
    df[num_columns] = df_num.replace(np.nan, 0)
    ## non numerical columns
    df_not_num = df.select_dtypes(exclude=[np.number])
    not_num_columns = df_not_num.columns
    df[not_num_columns] = df_not_num.replace(np.nan, 'empty')

    # create req strings
    table_name = 'industry'
    columns = ','.join(df.columns.values)
    values = ("%s, " * len(df.columns))[:-2]
    req = """INSERT IGNORE INTO %s (%s) VALUES (%s)""" % (table_name, columns, values)


    # insert MySQL
    mysql_cursor = db.cursor()
    chunk_size = 1000
    for i in range(0, len(df.index), chunk_size):
        chunk_df = df.iloc[i: i + chunk_size]
        data = [tuple(x) for x in chunk_df.values.tolist()]
        mysql_cursor.executemany(req, data)
        db.commit()

    mysql_cursor.close()

if __name__ == '__main__':
    # insert Global industry info
    file_name_global = '20210101_Industry_Global.csv'
    insert_industry_data_into_db(file_name_global)
    # insert US industry info
    file_name_us = '20210101_Industry_US.csv'
    insert_industry_data_into_db(file_name_us)