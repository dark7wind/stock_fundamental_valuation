import yaml
import MySQLdb as mdb
from definitions import DATABASE_CONFIG_DIR
import pandas as pd
pd.set_option('display.max_columns', None)
from src.valuation.valuation_single_stock import *

def valuation_multiple_stock():
    # load the database configuration
    with open(DATABASE_CONFIG_DIR) as f:
        db_config = yaml.load(f, Loader=yaml.FullLoader)

    db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                     db=db_config['db_name'], use_unicode=True, charset="utf8")

    # get the tickers
    # select stockId and ticker from table stock_info
    table_name = 'stock_info'
    columns = ','.join(['stockId', 'ticker'])
    req = """SELECT %s FROM %s WHERE dow=TRUE """ % (columns, table_name)
    get_ticker_cursor = db.cursor()
    get_ticker_cursor.execute(req)
    stockId_ticker = get_ticker_cursor.fetchall()
    get_ticker_cursor.close()

    for stock_id, ticker in stockId_ticker:
        estimated_value, price_to_value = valuation_single_stock(ticker)
        print(f'stock: {ticker}, estimated_value: {estimated_value}, price_to_value: {price_to_value}')

    1

if __name__ == '__main__':
    valuation_multiple_stock()