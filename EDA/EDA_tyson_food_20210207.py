import yahoofinancials as yf
import pickle
from src.firm_valuation import *

#%%
ticker = 'TSN'
yahoo_financials = yf.YahooFinancials(ticker)


read_from_yahoo = False

if read_from_yahoo:
    ## Get financial statements
    #%%
    # all_statement_data_qt =  yahoo_financials.get_financial_stmts('quarterly', ['income', 'cash', 'balance'])
    # all_statement_data_qt
    #%%
    all_statement_data_yr =  yahoo_financials.get_financial_stmts('annual', ['income', 'cash', 'balance'])
    with open('./data/20210207_TSN_all_statement_yr.pickle', 'wb') as handle:
        pickle.dump(all_statement_data_yr, handle, protocol=pickle.HIGHEST_PROTOCOL)

else:
    with open('./data/20210207_TSN_all_statement_yr.pickle', 'rb') as handle:
        all_statement_data_yr = pickle.load(handle)

balance_sheet = all_statement_data_yr['balanceSheetHistory']['TSN']
current_balance_sheet = balance_sheet[0]
current_date = [*current_balance_sheet.keys()][0]
current_balance_sheet = current_balance_sheet[current_date]
print(f'currnet_date: {current_date}')

income_statement = all_statement_data_yr['incomeStatementHistory']['TSN']
current_income_statement =income_statement[0]
current_date = [*current_income_statement.keys()][0]
current_income_statement = current_income_statement[current_date]
print(f'currnet_date: {current_date}')

## input
## to do make input function / class
revenue_current = current_income_statement['totalRevenue']
debt_bv = current_balance_sheet['shortLongTermDebt'] + current_balance_sheet['longTermDebt']
cash_value = current_balance_sheet['cash']
non_operating_assets = 0
value_options = 0
num_share = 294790000
price_current = 64.75

growth_list = [0.02, 0.02, 0.02, 0.02, 0.02, 0.0182, 0.0164, 0.0147, 0.0129, 0.0111]
margin_list = [0.07, 0.066, 0.064, 0.062, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06]
tax_rate_list = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
nol_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sales_to_capital_list = [1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36]
cost_capital_list = [0.065, 0.065, 0.065, 0.065, 0.065, 0.0641, 0.0632, 0.0623, 0.0614, 0.0605]
tax_terminal = 0.25
terminal_roic = 0.0605
terminal_cost_capital = 0.0605

prob_failure = 0
proceeds_failure = 0
minority_interests = 0
lease_flag = True
lease_to_debt = 520971240



## present value --> growth period
pv_growth, revenue_list, present_value_list= present_value_growth_period_func(revenue_current, growth_list, \
                                                                         margin_list, tax_rate_list, \
                                                                         nol_list, sales_to_capital_list, \
                                                                         cost_capital_list)
print(f'present value in growth period: {pv_growth}')
print(f'list of revenue: {revenue_list}')

## present_value --> terminal period
pv_terminal = present_value_terminal_func(revenue_list, growth_list[-1], margin_list, tax_terminal, \
                                     terminal_roic, terminal_cost_capital, cost_capital_list)
print(f'present value in growth period: {pv_terminal}')

## sum of present value
pv_sum = pv_growth + pv_terminal
print(f'pv_sum: {pv_sum}')

## operating assets value
operating_assets_value = value_operating_assets_func(pv_terminal, pv_growth, prob_failure, proceeds_failure)
print(f'value of operating assets: {operating_assets_value}')

## debt
debt_value = debt_func(debt_bv, lease_flag, lease_to_debt)
print(f'value of debt: {debt_value}')

## common stock equity value
equity_value = equity_value_common_stock_func(operating_assets_value, debt_value, minority_interests, cash_value, \
                                         non_operating_assets, value_options)
print(f'common stock equity value: {equity_value}')

## estimated value
estimated_value, price_to_value = estimated_value_share_func(equity_value, num_share, price_current)
print(f'estimate value: {estimated_value}')
print(f'estimated value / price: {price_to_value}')