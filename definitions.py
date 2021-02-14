import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # project root
TICKERS_DIR = os.path.join(ROOT_DIR, 'data/tickers/')
INCOME_STATEMENT_DIR = os.path.join(ROOT_DIR, 'data/fundamental/income_statement/')
DATABASE_CONFIG_DIR = os.path.join(ROOT_DIR, 'database/database_config/database.ymal')
