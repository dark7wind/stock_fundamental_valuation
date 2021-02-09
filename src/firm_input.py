


def growth_list_direct_func(r_gr_next, r_gr_high, length_high_growth, length_high_growth_stable, r_riskfree,\
                            flag_gr_terminal_direct, r_gr_terminal_direct):
    """
    :param r_gr_next: growth rate next year
    :param r_gr_high: growth rate in high growth period
    :param length_high_growth: length of high growth period
    :param length_high_growth_stable: length of high and stable growth period
    :param r_riskfree:
    :param flag_gr_terminal_direct: flag if direct input terminal growth rate
    :param r_gr_terminal_direct:
    :return:
    """
    assert length_high_growth_stable < length_high_growth, "the converge period should be less than the high growth period"
    gr_list = list()

    if flag_gr_terminal_direct:
        r_gr_terminal = r_gr_terminal_direct
    else:
        r_gr_terminal = r_riskfree

    for i in range(1, length_high_growth+1):
        if i == 1:
            gr_list.append(r_gr_next)
        elif i <= length_high_growth_stable:
            gr_list.append(r_gr_high)
        else:
            r_gr = r_gr_high-((r_gr_high-r_gr_terminal)/(length_high_growth-length_high_growth_stable))*\
                   (i-length_high_growth_stable)
            gr_list.append(r_gr)
    return gr_list


def margin_list_direct_func(margin_next_year, margin_target, converge_year, length_high_growth):
    """
    :param margin_next_year: margin in next year
    :param margin_target: target margin
    :param converge_year: the length of period to converge to target margin
    :param length_high_growth: length of high growth period
    :return:
    """
    margin_list = list()
    for i in range(1, length_high_growth+1):
        if i == 1:
            margin = margin_next_year
            margin_list.append(margin)
        if i >1 and i <= converge_year:
            margin = margin_target-((margin_target-margin_next_year)/converge_year)*(converge_year-i)
            margin_list.append(margin)
        if i > converge_year:
            margin = margin_target
            margin_list.append(margin)
    return margin_list

def sales_to_capital_list_func(revenue, invested_capital, industry_us, industry_global, length_high_growth,\
                               flag='company'):
    if flag == "company":
        sales_to_capital = revenue/invested_capital
        return [sales_to_capital]*length_high_growth

    elif flag == "industry_us":
        sales_to_capital = industry_us
        return [sales_to_capital] * length_high_growth

    elif flag == "industry_global":
        sales_to_capital = industry_global
        return [sales_to_capital] * length_high_growth

    else:
        print('the flag should be one of the following: 1. company, 2. industry_us, 3. industry_global')


def tax_rate_list_func(net_income_before_tax, tax, r_marginal_tax, flag_terminal_tax,):
    pass


flag = "company"
revenue = 43185
invested_capital = 26037
length_high_growth = 10
industry_us = 1.36
industry_global = 1.66

test = sales_to_capital_list_func(revenue, invested_capital, industry_us, industry_global, length_high_growth,\
                                  flag='company')

1