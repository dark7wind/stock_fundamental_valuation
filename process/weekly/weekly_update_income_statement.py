from src.database.update_table_income_statement_sp500 import insert_updated_income_statement_sp500_into_db
from src.database.update_table_income_statement_nyse import insert_updated_income_statement_nyse_into_db
from src.database.update_table_income_statement_nasdaq import insert_updated_income_statement_nasdaq_into_db

insert_updated_income_statement_sp500_into_db()
print('complete update income statement sp500')

insert_updated_income_statement_nyse_into_db()
print('complete update income statement nyse')

insert_updated_income_statement_nasdaq_into_db()
print('complete update income statement nasdaq')
