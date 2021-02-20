import unittest

from src.valuation.valuation_input_list import growth_list_direct_func, margin_list_direct_func, sales_to_capital_list_func, \
                           tax_rate_list_func

class TestFirmInput(unittest.TestCase):
    def test_growth_list_direct_func(self):
        """
        :return:
        """
        # test case 1
        r_gr_next = 0.02
        r_gr_high = 0.02
        length_high_growth = 10
        length_high_growth_stable = 5
        r_riskfree = 0.0111
        flag_gr_terminal_direct = False
        r_gr_terminal_direct = 0.02
        result = growth_list_direct_func(r_gr_next, r_gr_high, length_high_growth, length_high_growth_stable,\
                                         r_riskfree, flag_gr_terminal_direct, r_gr_terminal_direct)
        self.assertEqual(result, [0.02, 0.02, 0.02, 0.02, 0.02, 0.01822, 0.01644, 0.014660000000000001, 0.01288, 0.0111])

    def test_margin_list_direct_func(self):
        """
        :return:
        """
        # test case 1
        margin_next_year = 0.07
        margin_target = 0.06
        converge_year = 5
        length_high_growth = 10
        result = margin_list_direct_func(margin_next_year, margin_target, converge_year, length_high_growth)
        self.assertEqual(result, [0.07, 0.066, 0.064, 0.062, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06])

    def test_sales_to_capital_list_func(self):
        """
        :return:
        """
        # test case 1
        flag = "company"
        revenue = 43185
        invested_capital = 26037
        length_high_growth = 10
        industry_us = 1.36
        industry_global = 1.66
        result = sales_to_capital_list_func(revenue, invested_capital, industry_us, industry_global,\
                                            length_high_growth, flag)
        self.assertEqual(result, [1.658601221338864]*length_high_growth)

        # test case 2
        flag = "industry_us"
        revenue = 43185
        invested_capital = 26037
        length_high_growth = 10
        industry_us = 1.36
        industry_global = 1.66
        result = sales_to_capital_list_func(revenue, invested_capital, industry_us, industry_global, \
                                            length_high_growth, flag)
        self.assertEqual(result, [1.36] * length_high_growth)

    def test_tax_rate_list_func(self):
        """
        :return:
        """
        # test case 1
        effective_tax_rate = 0.25
        marginal_tax_rate = 0.25
        length_high_growth = 10
        length_high_growth_stable = 5
        flag_terminal_tax = True

        result = tax_rate_list_func(effective_tax_rate, marginal_tax_rate, length_high_growth,\
                                    length_high_growth_stable, flag_terminal_tax)
        self.assertEqual(result, [0.25]*10)

        # test case 2
        effective_tax_rate = 0.2
        marginal_tax_rate = 0.25
        length_high_growth = 10
        length_high_growth_stable = 6
        flag_terminal_tax = True

        result = tax_rate_list_func(effective_tax_rate, marginal_tax_rate, length_high_growth, \
                                    length_high_growth_stable, flag_terminal_tax)
        self.assertEqual(result, [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.21250000000000002, 0.22500000000000003, \
                                  0.23750000000000004, 0.25000000000000006])