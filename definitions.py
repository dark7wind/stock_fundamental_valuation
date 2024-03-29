import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # project root
TICKERS_DIR = os.path.join(ROOT_DIR, 'data/tickers/')
INCOME_STATEMENT_DIR = os.path.join(ROOT_DIR, 'data/fundamental/income_statement/')
BALANCE_SHEET_DIR = os.path.join(ROOT_DIR, 'data/fundamental/balance_sheet/')
CASH_FLOW_DIR = os.path.join(ROOT_DIR, 'data/fundamental/cash_flow/')
STATISTICS_DIR = os.path.join(ROOT_DIR, 'data/fundamental/statistics/')
HISTORICAL_PRICE_DIR = os.path.join(ROOT_DIR, 'data/historical_price/')
ANALYSIS_INFO_DIR = os.path.join(ROOT_DIR, 'data/fundamental/analysis_info/')
PROFILE_DIR = os.path.join(ROOT_DIR, 'data/fundamental/profile/')
INDUSTRY_DIR = os.path.join(ROOT_DIR, 'data/fundamental/industry/')

DATABASE_CONFIG_DIR = os.path.join(ROOT_DIR, 'database/database_config/database.ymal')
INPUT_DIR = os.path.join(ROOT_DIR, 'input/')
INPUT_DETAIL_STOCK_DIR = os.path.join(ROOT_DIR, 'result/stock_detail_analysis/')
RESULT_DIR = os.path.join(ROOT_DIR, 'result/')