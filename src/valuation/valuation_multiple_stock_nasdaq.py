import yaml
import MySQLdb as mdb
import datetime
from definitions import DATABASE_CONFIG_DIR, RESULT_DIR
import pandas as pd
pd.set_option('display.max_columns', None)
from src.valuation.valuation_single_stock import *

def valuation_multiple_stock(input_config_dir, input_config_file):
    # load the database configuration
    with open(DATABASE_CONFIG_DIR) as f:
        db_config = yaml.load(f, Loader=yaml.FullLoader)

    db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                     db=db_config['db_name'], use_unicode=True, charset="utf8")

    # get the tickers
    # select stockId and ticker from table stock_info
    table_name = 'stock_info'
    columns = ','.join(['stockId', 'ticker'])
    req = """SELECT %s FROM %s WHERE exchange='NASDAQ' """ % (columns, table_name)
    get_ticker_cursor = db.cursor()
    get_ticker_cursor.execute(req)
    stockId_ticker = get_ticker_cursor.fetchall()
    get_ticker_cursor.close()

    ticker_list = list()
    estimated_value_list = list()
    current_price_list = list()
    price_to_value_list = list()
    n = 1
    for stock_id, ticker in stockId_ticker:
        estimated_value, current_price, price_to_value = valuation_single_stock(ticker, input_config_dir, input_config_file)
        print(f'number: {n}, stock: {ticker}, estimated_value: {estimated_value}, price_to_value: {price_to_value}')
        ticker_list.append(ticker)
        estimated_value_list.append(estimated_value)
        current_price_list.append(current_price)
        price_to_value_list.append(price_to_value)
        n += 1

    df_valuation = pd.DataFrame(list(zip(ticker_list, current_price_list, estimated_value_list, price_to_value_list)),
                                columns =['ticker', 'current_price', 'estimated_value', 'price_to_value'])
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_name = 'valuation_result_nasdaq.csv'

    df_valuation.to_csv(RESULT_DIR + file_date + '_' + file_name, index=False)
    1

if __name__ == '__main__':
    input_config_dir = INPUT_DIR
    input_config_file = 'input.ymal'
    valuation_multiple_stock(input_config_dir, input_config_file)