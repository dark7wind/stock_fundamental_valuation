import yahoofinancials as yf
import pickle
from src.valuation.valuation_fcff import *
from src.valuation.back_up.valuation_input_list import *

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

## financial statement input
revenue_current = current_income_statement['totalRevenue']
income_before_tax = current_income_statement['incomeBeforeTax']
income_tax_expense = current_income_statement['incomeTaxExpense']
debt_bv = current_balance_sheet['shortLongTermDebt'] + current_balance_sheet['longTermDebt']
cash_value = current_balance_sheet['cash']
minority_interests = current_balance_sheet['minorityInterest']
non_operating_assets = 0
value_options = 0
num_share = 294790000
price_current = 64.75
effective_tax_rate_current = effective_tax_rate_func(income_before_tax, income_tax_expense, marginal_tax_rate, \
                                                     estimate_effective_tax_rate=0.25, flag_avg=False)
minority_interests = 0


## user manual input
r_gr_next = 0.02
r_gr_high = 0.02
length_high_growth = 10
length_high_growth_stable = 5
margin_next_year = 0.07
margin_target = 0.06
converge_year = 5
r_riskfree = 0.0111
sales_to_capital_flag = "industry_us"
invested_capital = 26037 # to do
industry_us = 1.36
industry_global = 1.66

effective_tax_rate = 0.25
marginal_tax_rate = 0.25

## R&D capitalization


## Lease capitalization
lease_flag = True
lease_to_debt = 520971240

## default assumption
flag_gr_terminal_direct = False
r_gr_terminal_direct = 0.02

flag_terminal_tax = True

nol_initial_flag = False
net_income_loss_previous = 0
tax_terminal = 0.25
terminal_roic = 0.0605
terminal_cost_capital = 0.0605
prob_failure = 0
proceeds_failure = 0


## output
# growth_list = [0.02, 0.02, 0.02, 0.02, 0.02, 0.0182, 0.0164, 0.0147, 0.0129, 0.0111]
growth_list = growth_list_direct_func(r_gr_next, r_gr_high, length_high_growth, length_high_growth_stable,\
                                      r_riskfree, flag_gr_terminal_direct, r_gr_terminal_direct)
# margin_list = [0.07, 0.066, 0.064, 0.062, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06]
margin_list = margin_list_direct_func(margin_next_year, margin_target, converge_year, length_high_growth)
# sales_to_capital_list = [1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36]
sales_to_capital_list = sales_to_capital_list_func(revenue_current, invested_capital, industry_us, industry_global, \
                                                   length_high_growth, sales_to_capital_flag)
# tax_rate_list = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
tax_rate_list = tax_rate_list_func(effective_tax_rate, marginal_tax_rate, length_high_growth, length_high_growth_stable,\
                                   flag_terminal_tax)

# nol_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
revenue_list = revenue_list_func(revenue_current, growth_list, length_high_growth)
ebit_list = ebit_list_func(revenue_list, margin_list)
nol_list = net_income_list_loss_func(net_income_loss_previous, ebit_list, length_high_growth, nol_initial_flag)


## cost of capital
cost_capital_list = [0.065, 0.065, 0.065, 0.065, 0.065, 0.0641, 0.0632, 0.0623, 0.0614, 0.0605]







## present value --> growth period
pv_growth, present_value_list= present_value_growth_period_func(revenue_list, ebit_list, growth_list,\
                                                                margin_list, tax_rate_list, nol_list, \
                                                                sales_to_capital_list, cost_capital_list)
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

1