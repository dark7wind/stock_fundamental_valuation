import MySQLdb as mdb
import pandas as pd
import datetime
import numpy as np
import yaml
from definitions import DATABASE_CONFIG_DIR, TICKERS_DIR
from src.data.get_ticker import get_ticker

# load the database configuration
with open(DATABASE_CONFIG_DIR) as f:
    db_config = yaml.load(f, Loader=yaml.FullLoader)

# # Obtain a database connection to the MySQL instance
# db_host = 'localhost'
# db_user = 'root'
# db_pass = 'password'
# db_name = 'securities_database'

db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                 db=db_config['db_name'], use_unicode=True, charset="utf8")

df = pd.DataFrame()
def insert_stock_info_data_into_db(load_local=False):
    # create the time now (utc time)
    now = datetime.datetime.utcnow()

    # get tickers
    if load_local:
        file_name = 'all_tickers.csv'
        df = pd.read_csv(TICKERS_DIR+file_name)
    else:
        df = get_ticker()

    df['createdDate'] = now
    df['lastUpdatedDate'] = now

    # covert nan to empty
    df = df.replace(np.nan, 'empty')
    # create req strings
    table_name = 'stock_info'
    columns = ','.join(df.columns.values)
    values = ("%s, " * len(df.columns))[:-2]
    req = """INSERT INTO %s (%s) VALUES (%s)""" % (table_name, columns, values)

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
    load_local = False
    insert_stock_info_data_into_db(load_local)
