import MySQLdb as mdb
import os
import yaml
import datetime
from src.data.get_fundamental_data_single_stock import get_income_statement_single_stock_yearly, \
    get_income_statement_single_stock_quarterly
from yahoo_fin.stock_info import *
from definitions import DATABASE_CONFIG_DIR, INCOME_STATEMENT_DIR



def download_income_statement():
    file_date = datetime.datetime.utcnow()
    file_date = file_date.strftime("%Y%m%d")
    file_income_statement = 'income_statement_sp500.csv'

    if os.path.exists(INCOME_STATEMENT_DIR+file_date+'_'+file_income_statement):
        df_income_statement_total = pd.read_csv(INCOME_STATEMENT_DIR+file_date+'_'+file_income_statement)
        # print(df_income_statement_total.columns)
        return df_income_statement_total
    else:
        # connect the databasefrom yahoo_fin.stock_info import *
        with open(DATABASE_CONFIG_DIR) as f:
            db_config = yaml.load(f, Loader=yaml.FullLoader)

        db = mdb.connect(host=db_config['db_host'], user=db_config['db_user'], passwd=db_config['db_pass'],
                         db=db_config['db_name'], use_unicode=True, charset="utf8")

        # select stockId and ticker from table stock_info
        table_name = 'stock_info'
        columns = ','.join(['stockId', 'ticker'])
        req = """SELECT %s FROM %s WHERE sp500=TRUE """ % (columns, table_name)
        get_ticker_cursor = db.cursor()
        get_ticker_cursor.execute(req)
        stockId_ticker = get_ticker_cursor.fetchall()
        get_ticker_cursor.close()

        # get the income_statement data from Yahoo
        df_income_statement_yearly_total = pd.DataFrame()
        df_income_statement_quarterly_total = pd.DataFrame()
        for stock_id, ticker in stockId_ticker:
            print(f'stockId: {stock_id}, ticker: {ticker}')
            df_income_statement_yearly = get_income_statement_single_stock_yearly(stock_id, ticker)
            df_income_statement_yearly_total = df_income_statement_yearly_total.append(df_income_statement_yearly,
                                                                                       ignore_index=True)
            df_income_statement_quarterly = get_income_statement_single_stock_quarterly(stock_id, ticker)
            df_income_statement_quarterly_total = df_income_statement_quarterly_total.append(
                df_income_statement_quarterly, ignore_index=True)


        # concat two dataframes
        df_income_statement_total = pd.concat([df_income_statement_yearly_total, df_income_statement_quarterly_total])

        # write to csv
        df_income_statement_total.to_csv(INCOME_STATEMENT_DIR+file_date+'_'+file_income_statement, index=False)
        # print(df_income_statement_total.columns)
        return df_income_statement_total


if __name__ == '__main__':
    download_income_statement()