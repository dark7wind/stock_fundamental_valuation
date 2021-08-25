from src.database.update_table_historical_price_sp500 import insert_updated_price_sp500_into_db
from src.database.update_table_historical_price_nyse import insert_updated_price_nyse_into_db
from src.database.update_table_historical_price_nasdaq import insert_updated_price_nasdaq_into_db

def weekly_update_historical_price():
    #insert_updated_price_sp500_into_db
    print('complete update historical price sp500')

    insert_updated_price_nyse_into_db()
    print('complete update historical price nyse')

    insert_updated_price_nasdaq_into_db()
    print('complete update historical price nasdaq')

if __name__ == '__main__':
    weekly_update_historical_price()