import yaml
from definitions import INPUT_DIR
from src.valuation.valuation_input_finance import get_input_finance_func, get_input_price_func, \
    get_analysis_estimate_revenue, get_historical_margin
from src.valuation.valuation_fcff import *
#from src.valuation.valuation_input_list import *


LOAD_TTM = True

def valuation_single_stock(ticker, manual_input=True):
    # load manual input
    with open(INPUT_DIR) as f:
        input_manual = yaml.load(f, Loader=yaml.FullLoader)

    # load manual default assumption
    mature_ERP = input_manual['mature_ERP']
    ## default assumption
    flag_cost_capital_terminal_override = input_manual['flag_cost_capital_terminal_override']
    cost_capital_terminal_override = input_manual['cost_capital_terminal_override']
    flag_risk_free_terminal_override = input_manual['flag_risk_free_terminal_override']
    risk_free_terminal_override = input_manual['risk_free_terminal_override']
    flag_gr_terminal_direct = input_manual['flag_gr_terminal_direct']
    r_gr_terminal_direct = input_manual['r_gr_terminal_direct']
    flag_terminal_tax = input_manual['flag_terminal_tax']
    nol_initial_flag = input_manual['nol_initial_flag']
    net_income_loss_previous = input_manual['net_income_loss_previous']
    tax_terminal = input_manual['tax_terminal']
    terminal_roic = input_manual['terminal_roic']
    prob_failure = input_manual['prob_failure']
    proceeds_failure = input_manual['proceeds_failure']

    try:
        ## load income statement and balance sheet
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

        print(f'ticker: {ticker}')
        print(f'current year revenue: {total_revenue}')
        print(f'current year income before tax: {income_before_tax}')
        print(f'current year tax expense: {income_tax_expense}')

        short_term_debt = df_balance_sheet_current['shortLongTermDebt'].iloc[0]
        long_term_debt = df_balance_sheet_current['longTermDebt'].iloc[0]
        debt_bv = short_term_debt + long_term_debt
        equity_bv = df_balance_sheet_current['totalStockholderEquity'].iloc[0]
        cash = df_balance_sheet_current['cash'].iloc[0]
        minority_interests = df_balance_sheet_current['minorityInterest'].iloc[0]
        non_operating_assets = 0 # default (to do)
        options = 0 # default (to do)
        print(f'book value of debt: {debt_bv}')
        print(f'book value of equity: {equity_bv}')
        print(f'cash and marketable securities: {cash}')
        print(f'minority interest: {minority_interests}')
        print(f'non operating assets: {non_operating_assets}')
        print(f'options: {options}')


        ## outstanding shares
        df_stock_statics_current = df_stock_statics.loc[df_stock_statics['lastUpdatedDate'] == \
                                                                     df_stock_statics['lastUpdatedDate'].max()]
        num_share = df_stock_statics_current['sharesOutstanding'].iloc[0]
        if num_share[-1] == 'B':
            num_share = float(num_share[: -1]) * 10**9
        elif num_share[-1] == 'M':
            num_share = float(num_share[: -1]) * 10**6
        print(f'number of shares outstanding: {num_share}')

        ## current price
        price_current = get_input_price_func(ticker)['close'].iloc[0]
        print(f'current price: {price_current}')

        ## tax
        marginal_tax_rate = 0.25
        effective_tax_rate = effective_tax_rate_func(income_before_tax, income_tax_expense, marginal_tax_rate,
                                                     estimate_effective_tax_rate=0.25, flag_avg=False)
        print(f'marginal tax rate: {marginal_tax_rate}')
        print(f'effective tax rate: {effective_tax_rate}')

        ## invested capital
        invested_capital = invested_capital_func(equity_bv, debt_bv, cash)
        print(f'invested capital: {invested_capital}')

        ## growth
        growth_input = 'analysis'
        if growth_input == 'manual':
            r_gr_next = input_manual['r_gr_next']
            r_gr_high = input_manual['r_gr_high']
        elif growth_input == 'analysis':
            r_gr_next, r_gr_high = get_analysis_estimate_revenue(ticker)

        length_high_growth = input_manual['length_high_growth']
        length_high_growth_stable = input_manual['length_high_growth_stable']


        ## margin
        margin_input = 'historical_mean'
        if margin_input == 'manual':
            margin_next_year = input_manual['margin_next_year']
            margin_target = input_manual['margin_target']
        elif margin_input == 'historical_mean':
            margin_historical_mean, margin_historical_recent = get_historical_margin(ticker)
            margin_next_year = margin_historical_mean
            margin_target = margin_historical_mean
        elif margin_input == 'historical_recent':
            margin_historical_mean, margin_historical_recent = get_historical_margin(ticker)
            margin_next_year = margin_historical_recent
            margin_target = margin_historical_recent

        converge_year = input_manual['converge_year']
        print(f'margin next year: {margin_next_year}, margin target: {margin_target}, converge year: {converge_year}')

        ## R&D capitalization (to do)

        ## Lease capitalization (to do)
        flag_lease = input_manual['flag_lease']
        lease_to_debt = 0  # to do

        ## risk free rate
        r_riskfree = input_manual['r_riskfree']

        ## growth list
        growth_list = growth_list_direct_func(r_gr_next, r_gr_high, length_high_growth, length_high_growth_stable, \
                                              r_riskfree, flag_gr_terminal_direct, r_gr_terminal_direct)
        print(f'growth_list: {growth_list}')

        ## margin list
        margin_list = margin_list_direct_func(margin_next_year, margin_target, converge_year, length_high_growth)
        print(f'margin list: {margin_list}')

        ## sales to capital list
        flag_sales_to_capital = input_manual['flag_sales_to_capital']
        sales_to_capital_us = 0 ## to do
        sales_to_capital_global = 0 ## to do
        sales_to_capital_list = sales_to_capital_list_func(total_revenue, invested_capital, sales_to_capital_us,
                                                           sales_to_capital_global, length_high_growth,
                                                           flag_sales_to_capital)
        print(f'sales to capita list: {sales_to_capital_list}')

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
        #cost_capital_list = [0.065, 0.065, 0.065, 0.065, 0.065, 0.0641, 0.0632, 0.0623, 0.0614, 0.0605]
        if input_manual['cost_capital_manual'] == True:
            cost_capital = input_manual['cost_capital']
        else:
            pass
        cost_capital_list = cost_of_capital_list_func(cost_capital, length_high_growth, length_high_growth_stable,
                                                      r_riskfree, mature_ERP, risk_free_terminal_override,
                                                      cost_capital_terminal_override, flag_risk_free_terminal_override,
                                                      flag_cost_capital_terminal_override)
        print(f'cost of capital list: {cost_capital_list}')

        ## present value -> growth period
        pv_growth, present_value_list = present_value_growth_period_func(revenue_list, ebit_list, growth_list, \
                                                                         margin_list, tax_rate_list, nol_list, \
                                                                         sales_to_capital_list, cost_capital_list)
        print(f'present value in growth period: {pv_growth}')

        ## present_value -> terminal period
        pv_terminal = present_value_terminal_func(revenue_list, growth_list[-1], margin_list, tax_terminal, \
                                                  terminal_roic, cost_capital_list)
        print(f'present value in growth period: {pv_terminal}')

        ## sum of present value
        pv_sum = pv_growth + pv_terminal
        print(f'pv_sum: {pv_sum}')

        ## operating assets value
        operating_assets_value = value_operating_assets_func(pv_terminal, pv_growth, prob_failure, proceeds_failure)
        print(f'value of operating assets: {operating_assets_value}')

        ## debt
        debt_value = debt_func(debt_bv, flag_lease, lease_to_debt)
        print(f'value of debt: {debt_value}')

        ## common stock equity value
        equity_value = equity_value_common_stock_func(operating_assets_value, debt_value, minority_interests, cash, \
                                                      non_operating_assets, options)
        print(f'common stock equity value: {equity_value}')

        ## estimated value
        estimated_value, price_to_value = estimated_value_share_func(equity_value, num_share, price_current)
        print(f'estimate value: {estimated_value}')
        print(f'price / estimated value: {price_to_value}')

    except:
        print('exists error')
        estimated_value = np.nan
        price_current = np.nan
        price_to_value = np.nan

    return estimated_value, price_current, price_to_value



if __name__ == '__main__':
    ticker = 'KR' #'TSN', 'KR' 'ODFL'
    valuation_single_stock(ticker)