import numpy as np

def ebit_base_margin_func(ebit, revenues):
    """
    :param ebit: EBIT (operating income)
    :param revenues: Revenue
    :return:
    """
    return ebit/revenues

def ebit_base_year_func():
    pass

def nol_func(revenue, nol_pre_y):
    """
    :param revenue: Revenue current year
    :param nol_pre_y: Net Operation Loss in the previous year
    :return:
    """
    if revenue < 0:
        return nol_pre_y - revenue
    else:
        if nol_pre_y > revenue:
            return nol_pre_y - revenue
        else:
            return 0

def after_tax_ebit_func(ebit, nol_pre_y, tax_rate):
    """
    :param ebit: EBIT (operating income)
    :param nol_pre_y: previous year net operating loss
    :param tax_rate: effective tax rate
    :return: after tax EBIT --> EBIT(1-tax)
    """
    if ebit > 0:
        if ebit < nol_pre_y:
            return ebit
        else:
            return ebit-(ebit-nol_pre_y)*tax_rate
    else:
        return ebit

def reinvestment_func(revenue_c, revenue_p, ratio_sales_capital):
    """
    :param revenue_c: Revenue current year
    :param reveune_p: Revenue previous year
    :param ratio_sales_capital: Sales to capital ratio
    :return:
    """
    if revenue_c > revenue_p:
        return (revenue_c - revenue_p)/ratio_sales_capital
    else:
        return 0

def fcff_func(after_tax_ebit, reinvestment):
    """
    :param after_tax_ebit: EBIT after tax
    :param reinvestment: reinvestment
    :return:
    """
    return after_tax_ebit - reinvestment

def present_value_func(cash_flow, discount_rate_list):
    """
    :param cash_flow: Cash Flow current year
    :param discount_rate_list: list of discount rates
    :return: present value
    """
    # n = len(discount_rate_list)
    cumulated_discount = 1
    for r in discount_rate_list:
        cumulated_discount = cumulated_discount*(1+r)
    return cash_flow/cumulated_discount

def terminal_value_func(cash_flow_terminal, cost_capital_terminal, growth_terminal):
    """
    :param cash_flow_terminal: cash flow terminal year
    :param cost_capital_terminal: cost of capital in terminal year
    :param growth_terminal: grwoth rate in terminal year
    :return:
    """
    return cash_flow_terminal/(cost_capital_terminal - growth_terminal)


def cost_capital_list_func():
    pass

def tax_rate_list_func():
    pass

def growth_rate_terminal_func():
    pass

def roic_terminal_func():
    pass

def cost_capital_terminal_func():
    pass

def present_value_growth_period_func(revenue_current, growth_list, margin_list, tax_rate_list, nol_list, \
                                sales_to_capital_list, cost_capital_list):
    assert (len(growth_list) == len(sales_to_capital_list) and len(growth_list) == len(margin_list) and \
            len(growth_list) == len(tax_rate_list) and len(growth_list) == len(cost_capital_list) and \
            len(growth_list) == len(nol_list)), \
        'Check the length of the list of growth, sales_to_capital and cost_capital'
    n = len(growth_list)
    # revenue
    revenue_list = list()
    revenue_list.append(revenue_current)
    revenue = revenue_current
    # present value
    present_value_list = list()

    for i in range(n):
        revenue_p = revenue
        revenue = revenue*(1+growth_list[i])
        ebit = revenue*margin_list[i]
        ebit_after_tax = after_tax_ebit_func(ebit, nol_list[i], tax_rate_list[i])
        value_reinvestment = reinvestment_func(revenue, revenue_p, sales_to_capital_list[i])
        value_fcff = fcff_func(ebit_after_tax, value_reinvestment)
        value_present = present_value_func(value_fcff, cost_capital_list[:i+1])

        revenue_list.append(revenue)
        present_value_list.append(value_present)

    present_value_total = np.sum(present_value_list)

    return present_value_total, revenue_list, present_value_list

def present_value_terminal_func(revenue_list, growth_rate_terminal, margin_list, tax_terminal, roic_terminal, \
                           cost_capital_terminal, cost_capital_list):

    # terminal fcff
    revenue_terminal = revenue_list[-1]*(1+growth_rate_terminal)
    margin_terminal = margin_list[-1]
    ebit = revenue_terminal*margin_terminal
    ebit_after_tax_terminal = ebit*(1-tax_terminal)
    if revenue_terminal > 0:
        reinvestment_terminal = (growth_rate_terminal/roic_terminal)*ebit_after_tax_terminal # growth_rate = reinvestment_rate_* roic
    else:
        reinvestment_terminal = 0
    fcff_terminal = fcff_func(ebit_after_tax_terminal, reinvestment_terminal)

    # terminal value
    value_terminal = terminal_value_func(fcff_terminal, cost_capital_terminal, growth_rate_terminal)
    terminal_present_value = present_value_func(value_terminal, cost_capital_list)
    return terminal_present_value

def proceeds_failure_func():
    pass

def value_operating_assets_func(present_value_terminal, present_value_growth_period, prob_failure, proceeds_failure):
    """
    :param present_value_sum: sum of present value of the company
    :param prob_failure: probability of company failure over  the foreseeable future
    :param proceeds_failure: distress proceeds as percentage of book or fair value
    :return:
    """
    present_value_sum = present_value_terminal + present_value_growth_period
    return present_value_sum*(1-prob_failure) + proceeds_failure*prob_failure

def debt_func(debt_bv, lease_flag, lease_to_debt):
    """
    :param debt_bv: book value of debt
    :param lease_flag: flag of lease converter
    :param lease_to_debt: lease convert to debt
    :return:
    """
    if lease_flag:
        return debt_bv + lease_to_debt
    else:
        return debt_bv

def cash_func(cash_securities, flag_foreign_trap=False, cash_trapped=0, tax_marginal=0.25, tax_foreign=0.15):
    """
    :param cash_securities: cash and marketable securities
    :param flag_foreign_trap:
    :param cash_trapped: cash trapped in foreign markets
    :param tax_marginal: marginal tax rate
    :param tax_foreign: average tax rate of foreign markets
    :return:
    """
    if flag_foreign_trap:
        return cash_securities - cash_trapped*(tax_marginal - tax_foreign)
    else:
        return cash_securities

def equity_value_common_stock_func(value_operating_assets, debt, minority_interests, cash, \
                              non_operating_assets, value_options):
    """
    :param value_operating_assets: value of operating assets
    :param debt: debt
    :param minority_interests: minority interests
    :param cash: cash
    :param non_operating_assets: value of non-operating assets
    :param value_options: value of options
    :return: equity value of common stock
    """
    return value_operating_assets - debt - minority_interests + cash + non_operating_assets - value_options

def estimated_value_share_func(equity_value, num_share, price_current):
    estimated_value = equity_value / num_share
    price_to_value = price_current / estimated_value
    return estimated_value, price_to_value



1