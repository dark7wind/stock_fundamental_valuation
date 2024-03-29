from src.database.update_table_cash_flow_sp500 import insert_updated_cash_flow_sp500_into_db
from src.database.update_table_cash_flow_nyse import insert_updated_cash_flow_nyse_into_db
from src.database.update_table_cash_flow_nasdaq import insert_updated_cash_flow_nasdaq_into_db

def weekly_update_cash_flow():
    insert_updated_cash_flow_sp500_into_db()
    print('complete update cash flow sp500')

    insert_updated_cash_flow_nyse_into_db()
    print('complete update cash flow nyse')

    insert_updated_cash_flow_nasdaq_into_db()
    print('complete update cash flow nasdaq')

if __name__ == '__main__':
    weekly_update_cash_flow()