from src.valuation.valuation_single_stock import valuation_single_stock
from definitions import INPUT_DETAIL_STOCK_DIR
from datetime import date
import os


# dd/mm/YY
ticker = 'MO'
input_config_dir = os.path.join(INPUT_DETAIL_STOCK_DIR, ticker+'/')

today = date.today()
date = today.strftime("%Y%m%d")
input_config_file = ticker + '_input_' + date + '.ymal'

estimated_value, price_current, price_to_value = valuation_single_stock(ticker, input_config_dir, input_config_file)