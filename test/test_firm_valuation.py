import unittest

from src.firm_valuation import after_tax_ebit, present_value, terminal_value, equity_value_common_stock, \
                               estimated_value_share, present_value_growth_period, present_value_terminal

class TestFirmValuation(unittest.TestCase):
    def test_after_tax_ebit(self):
        """
        Test case 1: EBIT>0, NOL=0 and EBIT>NOL
        """
        # test case 1: EBIT >0, NOL=0 and EBIT > NOL
        ebit = 3083.41
        nol_pre_y = 0
        tax_rate = 0.25
        result = after_tax_ebit(ebit, nol_pre_y, tax_rate)
        self.assertEqual(result, 2312.5575)

        # test case 2: EBIT<0,
        ebit = -3083.41
        nol_pre_y = 0
        tax_rate = 0.34
        result = after_tax_ebit(ebit, nol_pre_y, tax_rate)
        self.assertEqual(result, -3083.41)

        # test case 3: EBIT >0, NOL=!0 and EBIT > NOL
        ## to do

        # test case 4: EBIT >0, NOL=!0 and EBIT < NOL
        ## to do

    def test_present_value(self):
        """
        Test case 1: n_year = 1
        Test case 2: n_year > 1
        """
        # test case 1: n_year = 1
        cash_flow = 1677.48
        discount_rate_list = [0.065]
        result = round(present_value(cash_flow, discount_rate_list), 2)
        self.assertEqual(result, 1575.1)

        # test case 2: n_year > 1
        cash_flow = 1815.76
        discount_rate_list = [0.065, 0.065, 0.065, 0.065, 0.065]
        result = round(present_value(cash_flow, discount_rate_list), 2)
        self.assertEqual(result, 1325.29)

        # # test case 3: terminal year
        cash_flow = 44991.23
        discount_rate_list = [0.065, 0.065, 0.065, 0.065, 0.065, 0.0641, 0.0632, 0.0623, 0.0614, 0.0605]
        result = round(present_value(cash_flow, discount_rate_list), 2)
        self.assertEqual(result, 24274.23)

    def test_terminal_value(self):
        """
        Test case
        """
        cash_flow_terminal = 2222.57
        cost_capital_terminal = 0.0605
        growth_terminal = 0.0111
        result = round(terminal_value(cash_flow_terminal, cost_capital_terminal, growth_terminal))
        self.assertEqual(result, 44991)

    def test_equity_value_common_stock(self):
        """
        :return:
        """
        value_operating_assets = 37869.22
        debt = 11859.97
        minority_interests = 0
        cash = 1420
        non_operating_assets = 0
        value_options = 0
        result = equity_value_common_stock(value_operating_assets, debt, minority_interests, cash, \
                                           non_operating_assets, value_options)
        self.assertEqual(result, 27429.25)

    def test_estimated_value_share(self):
        """
        :return:
        """
        equity_value = 27429.25
        num_share = 294.79
        price_current = 64.75
        result1, result2 = estimated_value_share(equity_value, num_share, price_current)
        result1 = round(result1, 2)
        result2 = round(result2, 4)
        self.assertEqual((result1, result2), (93.05, 0.6959))

    def test_present_value_growth_period(self):
        """
        :return:
        """
        revenue_current = 43185
        growth_list = [0.02, 0.02, 0.02, 0.02, 0.02, 0.0182, 0.0164, 0.0147, 0.0129, 0.0111]
        margin_list = [0.07, 0.066, 0.064, 0.062, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06]
        tax_rate_list = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
        nol_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        sales_to_capital_list = [1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36, 1.36]
        cost_capital_list = [0.065, 0.065, 0.065, 0.065, 0.065, 0.0641, 0.0632, 0.0623, 0.0614, 0.0605]
        result1, result2, result3= present_value_growth_period(revenue_current, growth_list, margin_list, tax_rate_list, nol_list, \
                                             sales_to_capital_list, cost_capital_list)

        result1 = round(result1)
        result2 = round(result2[-1])
        result3 = round(result3[-1])
        self.assertEqual((result1, result2, result3), (11685, 51278, 1022))

    def test_present_value_terminal(self):
        """
        :return:
        """
        revenue_list = [44048.70, 44929.67, 45828.27, 46744.83, 47679.73, \
                        48548.45, 49346.59, 50070.01, 50714.91, 51277.85]
        growth_rate_terminal = 0.0111
        margin_list = [0.07, 0.066, 0.064, 0.062, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06]
        tax_terminal = 0.25
        roic_terminal = 0.0605
        cost_capital_terminal = 0.0605
        cost_capital_list = [0.065, 0.065, 0.065, 0.065, 0.065, 0.0641, 0.0632, 0.0623, 0.0614, 0.0605]
        result = present_value_terminal(revenue_list, growth_rate_terminal, margin_list, tax_terminal, roic_terminal, \
                                        cost_capital_terminal, cost_capital_list)
        result = round(result)
        self.assertEqual(result, 20806)

if __name__ == '__main__':
    unittest.main()
