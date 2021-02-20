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


def effective_tax_rate_func(taxable_income, tax_paid, marginal_tax_rate, estimate_effective_tax_rate=0.25, flag_avg=False):
    """
    You will find this in your company's annual report. If you cannot, you can compute it as follows,
    from the income statement: Effective tax rate = Taxes paid/ Taxable income
    If your effective tax rate varies across years, you can use an average. If the effective tax rate is less than zero,
    enter zero. If you have a money losing company, don't enter zero but enter the tax rate that you will have when you
    start making money.
    :param taxable_income:
    :param tax_paid:
    :param marginal_tax_rate:
    :param estimate_effective_tax_rate: if money losing company, estimate the effective tax rate when it starts to
           making money
    :param flag_avg: True: calculate the average effective tax rate
    :return:
    """
    if not flag_avg:
        effective_tax_rate = tax_paid / taxable_income
    else:
        pass # to do

    if effective_tax_rate < 0:
        effective_tax_rate = estimate_effective_tax_rate
    elif effective_tax_rate > 1:
        effective_tax_rate = marginal_tax_rate

    return effective_tax_rate

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
    """
    :param equity_value:
    :param num_share:
    :param price_current:
    :return:
    """
    estimated_value = equity_value / num_share
    price_to_value = price_current / estimated_value
    return estimated_value, price_to_value

def revenue_list_func(revenue_current, growth_list, length_high_growth):

    # revenue
    revenue = revenue_current
    revenue_list = list()
    revenue_list.append(revenue)
    for i in range(0, length_high_growth):
        revenue = revenue * (1 + growth_list[i])
        revenue_list.append(revenue)
    return revenue_list


def ebit_list_func(revenue_list, margin_list):
    ebit_list = [revenue * margin for revenue, margin in zip(revenue_list[1:], margin_list)]
    return ebit_list

def net_income_func(ebit, nol_pre_y):
    """
    :param ebit: EBIT -> operating income
    :param nol_pre_y: Net Operation Loss in the previous year
    :return:
    """
    if ebit < 0:
        return nol_pre_y - ebit
    else:
        if nol_pre_y > ebit:
            return nol_pre_y - ebit
        else:
            return 0

def net_income_list_loss_func(net_income_loss_previous, ebit_list, length_high_growth, flag):
    """
    :param net_income_loss_previous:
    :param ebit_list:
    :param length_high_growth:
    :param flag:
    :return:
    """
    nol_list = list()
    if not flag:
        nol_initial = 0
        # nol_list = [nol_initial]*length_high_growth
    else:
        nol_initial = net_income_loss_previous

    nol = nol_initial
    nol_list.append(nol)

    for i in range(0, length_high_growth):
        nol = net_income_func(ebit_list[i], nol)
        nol_list.append(nol)
    return nol_list[1:] # in valuation, only need the nol from year 1


def present_value_growth_period_func(revenue_list, ebit_list, growth_list, margin_list, tax_rate_list, nol_list, \
                                     sales_to_capital_list, cost_capital_list):
    assert (len(growth_list) == len(sales_to_capital_list) and len(growth_list) == len(margin_list) and \
            len(growth_list) == len(tax_rate_list) and len(growth_list) == len(cost_capital_list) and \
            len(growth_list) == len(nol_list)), \
        'Check the length of the list of growth, sales_to_capital and cost_capital'
    n = len(growth_list)
    # present value
    present_value_list = list()

    for i in range(n):
        revenue_previous = revenue_list[i]
        revenue_current = revenue_list[i+1]
        ebit_after_tax = after_tax_ebit_func(ebit_list[i], nol_list[i], tax_rate_list[i])
        value_reinvestment = reinvestment_func(revenue_current, revenue_previous, sales_to_capital_list[i])
        value_fcff = fcff_func(ebit_after_tax, value_reinvestment)
        value_present = present_value_func(value_fcff, cost_capital_list[:i+1])
        present_value_list.append(value_present)

    present_value_total = np.sum(present_value_list)

    return present_value_total, present_value_list



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



1