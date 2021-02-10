


def growth_list_direct_func(r_gr_next, r_gr_high, length_high_growth, length_high_growth_stable, r_riskfree,\
                            flag_gr_terminal_direct, r_gr_terminal_direct):
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


def margin_list_func():
    pass

def sales_to_capital_list_func():
    pass




r_gr_next = 0.02
r_gr_high = 0.02
length_high_growth = 10
length_high_growth_stable = 5
r_riskfree = 0.0111
flag_gr_terminal_direct = False
r_gr_terminal_direct = 0.02

test = growth_list_direct_func(r_gr_next, r_gr_high, length_high_growth, length_high_growth_stable, r_riskfree,\
                            flag_gr_terminal_direct, r_gr_terminal_direct)

1