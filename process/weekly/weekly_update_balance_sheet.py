from src.database.update_table_balance_sheet_sp500 import insert_updated_balance_sheet_sp500_into_db
from src.database.update_table_balance_sheet_nyse import insert_updated_balance_sheet_nyse_into_db
from src.database.update_table_balance_sheet_nasdaq import insert_updated_balance_sheet_nasdaq_into_db

insert_updated_balance_sheet_sp500_into_db()
print('complete update balance sheet sp500')

insert_updated_balance_sheet_nyse_into_db()
print('complete update balance sheet nyse')

insert_updated_balance_sheet_nasdaq_into_db()
print('complete update balance sheet nasdaq')
