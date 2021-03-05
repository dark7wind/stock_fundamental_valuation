from src.valuation.valuation_input_finance import get_input_finance_func, get_input_price_func, \
    get_analysis_estimate_revenue, get_historical_margin
from src.valuation.valuation_fcff import *
from src.valuation.valuation_input_list import *

LOAD_TTM = False

def valuation_single_stock(ticker, manual_input=True):
    if not LOAD_TTM:
        df_income_statement, df_balance_sheet, df_stock_statics = get_input_finance_func(ticker, read_from_sql=True,
                                                                                         read_TTM=False)
        df_income_statement_yearly = df_income_statement.loc[(df_income_statement['type'] == 'yearly')]
        df_balance_sheet_yearly = df_balance_sheet.loc[(df_balance_sheet['type'] == 'yearly')]

        ## to do -> use yearly or quarterly -> now use yearly
        df_income_statement_current = df_income_statement_yearly.loc[df_income_statement_yearly['endDate'] == \
                                                                     df_income_statement_yearly['endDate'].max()]
        df_balance_sheet_current = df_balance_sheet_yearly.loc[df_balance_sheet_yearly['endDate'] == \
                                                               df_balance_sheet_yearly['endDate'].max()]
        # total revenue, income before tax, income tax expense
        total_revenue = df_income_statement_current['totalRevenue'].iloc[0]
        income_before_tax = df_income_statement_current['incomeBeforeTax'].iloc[0]
        income_tax_expense = df_income_statement_current['incomeTaxExpense'].iloc[0]

    else:
        df_income_statement, df_balance_sheet, df_stock_statics = get_input_finance_func(ticker, read_from_sql=True,
                                                                                         read_TTM=True)
        df_income_statement_current = df_income_statement.loc[df_income_statement['LastUpdatedDate'] == \
                                                                      df_income_statement['LastUpdatedDate'].max()]
        df_balance_sheet_current = df_balance_sheet.loc[df_balance_sheet['endDate'] == \
                                                               df_balance_sheet['endDate'].max()]

        # total revenue, income before tax, income tax expense
        total_revenue = df_income_statement_current['TotalRevenue'].iloc[0] * 1000
        income_before_tax = df_income_statement_current['PretaxIncome'].iloc[0] * 1000
        income_tax_expense = df_income_statement_current['TaxProvision'].iloc[0] * 1000

    print(f'current year revenue: {total_revenue}')
    print(f'current year income before tax: {income_before_tax}')
    print(f'current year tax expense: {income_tax_expense}')


    short_term_debt = df_balance_sheet_current['shortLongTermDebt'].iloc[0]
    long_term_debt = df_balance_sheet_current['longTermDebt'].iloc[0]
    debt_bv = short_term_debt + long_term_debt
    print(f'book value of debt: {debt_bv}')
    equity_bv = df_balance_sheet_current['totalStockholderEquity'].iloc[0]
    print(f'book value of equity: {equity_bv}')

    cash = df_balance_sheet_current['cash'].iloc[0]
    print(f'cash and marketable securities: {cash}')
    minority_interests = df_balance_sheet_current['minorityInterest'].iloc[0]
    #minority_interests = 0
    print(f'minority interest: {minority_interests}')

    non_operating_assets = 0 # default (to do)
    print(f'non operating assets: {non_operating_assets}')
    options = 0 # default (to do)
    print(f'options: {options}')

    # outstanding shares
    df_stock_statics_current = df_stock_statics.loc[df_stock_statics['lastUpdatedDate'] == \
                                                                 df_stock_statics['lastUpdatedDate'].max()]
    num_share = df_stock_statics_current['sharesOutstanding'].iloc[0]
    if num_share[-1] == 'B':
        num_share = float(num_share[: -1]) * 10**9
    elif num_share[-1] == 'M':
        num_share = float(num_share[: -1]) * 10**6
    print(f'number of shares outstanding: {num_share}')

    # get the price from database
    price_current = get_input_price_func(ticker)['close'].iloc[0]
    print(f'current price: {price_current}')


    marginal_tax_rate = 0.25
    effective_tax_rate = effective_tax_rate_func(income_before_tax, income_tax_expense, marginal_tax_rate, \
                                                       estimate_effective_tax_rate=0.25, flag_avg=False)
    print(f'marginal tax rate: {marginal_tax_rate}')
    print(f'effective tax rate: {effective_tax_rate}')

    invested_capital = invested_capital_func(equity_bv, debt_bv, cash)
    print(f'invested capital: {invested_capital}')

    if manual_input:
        ## user manual input
        r_gr_next_manual = 0.02
        r_gr_high_manual = 0.02
        length_high_growth = 10
        length_high_growth_stable = 1
        margin_next_year_manual = 0.07 # KR -> 0.0266  TSN -> 0.07
        margin_target_manual = 0.07 # KR -> 0.0266  TSN -> 0.07
        converge_year = 10
        r_riskfree = 0.0147
        sales_to_capital_flag = "company"

        industry_us = 4.26 # to do
        industry_global = 3.03 # to do
    else:
        pass

    # growth rate
    growth_input = 'analysis'
    if growth_input == 'manual':
        r_gr_next = r_gr_next_manual
        r_gr_high = r_gr_high_manual
    elif growth_input == 'analysis':
        r_gr_next, r_gr_high = get_analysis_estimate_revenue(ticker)

    # margin
    margin_input = 'historical_mean'
    if margin_input == 'manual':
        margin_next_year = margin_next_year_manual
        margin_target = margin_target_manual
    elif margin_input == 'historical_mean':
        margin_historical_mean, margin_historical_recent = get_historical_margin(ticker)
        margin_next_year = margin_historical_mean
        margin_target = margin_historical_mean
    elif margin_input == 'historical_recent':
        margin_historical_mean, margin_historical_recent = get_historical_margin(ticker)
        margin_next_year = margin_historical_recent
        margin_target = margin_historical_recent
    print(f'margin next year: {margin_next_year}, margin target: {margin_target}')

    ## R&D capitalization

    ## Lease capitalization
    lease_flag = False #True
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
    print(f'growth_list: {growth_list}')

    ## margin list
    margin_list = margin_list_direct_func(margin_next_year, margin_target, converge_year, length_high_growth)
    print(f'margin list: {margin_list}')

    ## sales to capital list
    sales_to_capital_list = sales_to_capital_list_func(total_revenue, invested_capital, industry_us, industry_global, \
                                                       length_high_growth, sales_to_capital_flag)
    print(f'sales to capital list: {sales_to_capital_list}')

    ## tax rate list
    tax_rate_list = tax_rate_list_func(effective_tax_rate, marginal_tax_rate, length_high_growth,
                                       length_high_growth_stable, \
                                       flag_terminal_tax)
    print(f'tax rate list: {tax_rate_list}')

    ## revenue list
    revenue_list = revenue_list_func(total_revenue, growth_list, length_high_growth)
    print(f'revenue list: {revenue_list}')

    ## EBIT list
    ebit_list = ebit_list_func(revenue_list, margin_list)
    print(f'EBIT list: {ebit_list}')

    ## Net operating lost list
    nol_list = net_income_list_loss_func(net_income_loss_previous, ebit_list, length_high_growth, nol_initial_flag)
    print(f'Net operating lost list: {nol_list}')

    ## cost of capital list  ## to do
    cost_capital_list = [0.065, 0.065, 0.065, 0.065, 0.065, 0.0641, 0.0632, 0.0623, 0.0614, 0.0605]
    print(f'cost of capital list: {cost_capital_list}')

    ## present value --> growth period
    pv_growth, present_value_list = present_value_growth_period_func(revenue_list, ebit_list, growth_list, \
                                                                     margin_list, tax_rate_list, nol_list, \
                                                                     sales_to_capital_list, cost_capital_list)
    print(f'present value in growth period: {pv_growth}')

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
    print(f'price / estimated value: {price_to_value}')

    return estimated_value, price_to_value
    1


if __name__ == '__main__':
    ticker = 'TSN' #'TSN', 'KR'
    valuation_single_stock(ticker)