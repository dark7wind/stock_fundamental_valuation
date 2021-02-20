from src.valuation.valuation_input_finance import get_input_finance_func
from src.valuation.valuation_fcff import *
from src.valuation.valuation_input_list import *


def valuation_single_stock(ticker, manual_input=True):
    df_income_statement, df_balance_sheet = get_input_finance_func(ticker)
    df_income_statement_yearly = df_income_statement.loc[(df_income_statement['type']=='yearly')]
    df_balance_sheet_yearly = df_balance_sheet.loc[(df_balance_sheet['type']=='yearly')]

    ## to do -> use yearly or quarterly -> now use yearly
    df_income_statement_current = df_income_statement_yearly.loc[df_income_statement_yearly['endDate'] == \
                                                                 df_income_statement_yearly['endDate'].max()]
    df_balance_sheet_current = df_balance_sheet_yearly.loc[df_balance_sheet_yearly['endDate'] == \
                                                                 df_balance_sheet_yearly['endDate'].max()]


    total_revenue = df_income_statement_current['totalRevenue'][0]
    income_before_tax = df_income_statement_current['incomeBeforeTax'][0]
    income_tax_expense = df_income_statement_current['incomeTaxExpense'][0]

    short_term_debt = df_balance_sheet_current['shortLongTermDebt'][0]
    long_term_debt = df_balance_sheet_current['longTermDebt'][0]
    debt_bv = short_term_debt + long_term_debt

    cash = df_balance_sheet_current['cash'][0]
    minority_interests = df_balance_sheet_current['minorityInterest'][0]
    # minority_interests = 0 # temp

    non_operating_assets = 0 # default (to do)
    options = 0 # default (to do)
    num_share = 294790000 # to do --> extract from statistics
    price_current = 64.75 # to do --> extract from price database

    marginal_tax_rate = 0.25
    effective_tax_rate = effective_tax_rate_func(income_before_tax, income_tax_expense, marginal_tax_rate, \
                                                       estimate_effective_tax_rate=0.25, flag_avg=False)

    if manual_input:
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
        invested_capital = 26037  # to do
        industry_us = 1.36 # to do
        industry_global = 1.66 # to do
    else:
        pass

    ## R&D capitalization

    ## Lease capitalization
    lease_flag = True
    lease_to_debt = 520971240  # to do

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

    ## growth list
    growth_list = growth_list_direct_func(r_gr_next, r_gr_high, length_high_growth, length_high_growth_stable, \
                                          r_riskfree, flag_gr_terminal_direct, r_gr_terminal_direct)
    ## margin list
    margin_list = margin_list_direct_func(margin_next_year, margin_target, converge_year, length_high_growth)

    ## sales to capital list
    sales_to_capital_list = sales_to_capital_list_func(total_revenue, invested_capital, industry_us, industry_global, \
                                                       length_high_growth, sales_to_capital_flag)

    ## tax rate list
    tax_rate_list = tax_rate_list_func(effective_tax_rate, marginal_tax_rate, length_high_growth,
                                       length_high_growth_stable, \
                                       flag_terminal_tax)

    ## revenue list
    revenue_list = revenue_list_func(total_revenue, growth_list, length_high_growth)

    ## EBIT list
    ebit_list = ebit_list_func(revenue_list, margin_list)

    ## Net operating lost list
    nol_list = net_income_list_loss_func(net_income_loss_previous, ebit_list, length_high_growth, nol_initial_flag)

    ## cost of capital list  ## to do
    cost_capital_list = [0.065, 0.065, 0.065, 0.065, 0.065, 0.0641, 0.0632, 0.0623, 0.0614, 0.0605]

    ## present value --> growth period
    pv_growth, present_value_list = present_value_growth_period_func(revenue_list, ebit_list, growth_list, \
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
    equity_value = equity_value_common_stock_func(operating_assets_value, debt_value, minority_interests, cash, \
                                                  non_operating_assets, options)
    print(f'common stock equity value: {equity_value}')

    ## estimated value
    estimated_value, price_to_value = estimated_value_share_func(equity_value, num_share, price_current)
    print(f'estimate value: {estimated_value}')
    print(f'estimated value / price: {price_to_value}')

    return estimated_value, price_to_value
    1


if __name__ == '__main__':
    ticker = 'TSN'
    valuation_single_stock(ticker)