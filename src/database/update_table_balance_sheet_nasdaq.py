import MySQLdb as mdb
import pandas as pd
import datetime
import yaml
from src.data.download_balance_sheet_nasdaq import download_balance_sheet
from definitions import DATABASE_CONFIG_DIR


def insert_updated_balance_sheet_data_into_db():
    # load the database configuration
    with open(DATABASE_CONFIG_DIR) as f:
        db_config = yaml.load(f, Loader=yaml.FullLoader)

    db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                     db=db_config['db_name'], use_unicode=True, charset="utf8")

    # load balance sheet dataframe
    df = download_balance_sheet()

    # create the time now (utc time)
    now = datetime.datetime.utcnow()


    # to datetime
    #df['endDate'] = pd.to_datetime( df['endDate'])
    # createDate and lastUpdatedDate
    df['createdDate'] = now
    df['lastUpdatedDate'] = now


    # covert nan to empty
    df = df.fillna(0)

    # create req strings
    table_name = 'balance_sheet'
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
    insert_updated_balance_sheet_data_into_db()
