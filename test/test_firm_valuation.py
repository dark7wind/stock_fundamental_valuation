import unittest

from src.firm_valuation import after_tax_ebit_func, present_value_func, terminal_value_func, \
    equity_value_common_stock_func, estimated_value_share_func, present_value_growth_period_func, \
    present_value_terminal_func, effective_tax_rate_func, net_income_list_loss_func, revenue_list_func, \
    ebit_list_func

class TestFirmValuation(unittest.TestCase):
    def test_after_tax_ebit_func(self):
        """
        Test case 1: EBIT>0, NOL=0 and EBIT>NOL
        """
        # test case 1: EBIT >0, NOL=0 and EBIT > NOL
        ebit = 3083.41
        nol_pre_y = 0
        tax_rate = 0.25
        result = after_tax_ebit_func(ebit, nol_pre_y, tax_rate)
        self.assertEqual(result, 2312.5575)

        # test case 2: EBIT<0,
        ebit = -3083.41
        nol_pre_y = 0
        tax_rate = 0.34
        result = after_tax_ebit_func(ebit, nol_pre_y, tax_rate)
        self.assertEqual(result, -3083.41)

        # test case 3: EBIT >0, NOL=!0 and EBIT > NOL
        ## to do

        # test case 4: EBIT >0, NOL=!0 and EBIT < NOL
        ## to do

    def test_present_value_func(self):
        """
        Test case 1: n_year = 1
        Test case 2: n_year > 1
        """
        # test case 1: n_year = 1
        cash_flow = 1677.48
        discount_rate_list = [0.065]
        result = round(present_value_func(cash_flow, discount_rate_list), 2)
        self.assertEqual(result, 1575.1)

        # test case 2: n_year > 1
        cash_flow = 1458.16
        discount_rate_list = [0.065, 0.065, 0.065, 0.065, 0.065]
        result = round(present_value_func(cash_flow, discount_rate_list), 1)
        self.assertEqual(result, 1064.3)

        # # test case 3: terminal year
        cash_flow = 38563.91
        discount_rate_list = [0.065, 0.065, 0.065, 0.065, 0.065, 0.0641, 0.0632, 0.0623, 0.0614, 0.0605]
        result = round(present_value_func(cash_flow, discount_rate_list), 2)
        self.assertEqual(result, 20806.48)

    def test_terminal_value_func(self):
        """
        Test case
        """
        cash_flow_terminal = 1905.06
        cost_capital_terminal = 0.0605
        growth_terminal = 0.0111
        result = round(terminal_value_func(cash_flow_terminal, cost_capital_terminal, growth_terminal))
        self.assertEqual(result, 38564)

    def test_equity_value_common_stock_func(self):
        """
        :return:
        """
        value_operating_assets = 32491.19
        debt = 11859.97
        minority_interests = 0
        cash = 1420
        non_operating_assets = 0
        value_options = 0
        result = equity_value_common_stock_func(value_operating_assets, debt, minority_interests, cash, \
                                           non_operating_assets, value_options)
        self.assertEqual(result, 22051.22)

    def test_estimated_value_share_func(self):
        """
        :return:
        """
        equity_value = 22051.22
        num_share = 294.79
        price_current = 64.75
        result1, result2 = estimated_value_share_func(equity_value, num_share, price_current)
        result1 = round(result1, 2)
        result2 = round(result2, 4)
        self.assertEqual((result1, result2), (74.8, 0.8656))

    def test_present_value_growth_period_func(self):
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
        result1, result2, result3= present_value_growth_period_func(revenue_current, growth_list, margin_list, tax_rate_list, nol_list, \
                                             sales_to_capital_list, cost_capital_list)

        result1 = round(result1)
        result2 = round(result2[-1])
        result3 = round(result3[-1])
        self.assertEqual((result1, result2, result3), (11685, 51278, 1022))

    def test_present_value_terminal_func(self):
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
        result = present_value_terminal_func(revenue_list, growth_rate_terminal, margin_list, tax_terminal, roic_terminal, \
                                        cost_capital_terminal, cost_capital_list)
        result = round(result)
        self.assertEqual(result, 20806)

    def test_effective_tax_rate_func(self):
        """
        :return:
        """
        taxable_income = 2770000000
        tax_paid = 620000000
        marginal_tax_rate = 0.25
        result = effective_tax_rate_func(taxable_income, tax_paid, marginal_tax_rate, \
                                         estimate_effective_tax_rate=0.25, flag_avg=False)
        self.assertEqual(result, 0.22382671480144403)

    def test_net_income_list_loss_func(self):
        """
        :return:
        """
        # test case 1
        net_income_loss_previous = 100
        ebit_list = [80, 100, 100, 100, 100, 100, 200, 200, 200, 200]
        length_high_growth = 10
        flag = False
        result = net_income_list_loss_func(net_income_loss_previous, ebit_list, length_high_growth, flag)
        self.assertEqual(result, [0]*length_high_growth)

        # test case 2
        net_income_loss_previous = 100
        ebit_list = [80, 10, 100, 100, 100, 100, 200, 200, 200, 200]
        length_high_growth = 10
        flag = True
        result = net_income_list_loss_func(net_income_loss_previous, ebit_list, length_high_growth, flag)
        self.assertEqual(result, [20, 10, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_revenue_list_func(self):
        """
        :return:
        """
        revenue_current = 43185
        growth_list = [0.02, 0.02, 0.02, 0.02, 0.02, 0.0182, 0.0164, 0.0147, 0.0129, 0.0111]
        length_high_growth = 10
        result = revenue_list_func(revenue_current, growth_list, length_high_growth)
        self.assertEqual(result, [43185, 44048.700000000004, 44929.674000000006, 45828.26748000001, 46744.83282960001,\
                                  47679.72948619201, 48547.5005628407, 49343.67957207129, 50069.03166178073,\
                                  50714.9221702177, 51277.857806307125])

    def test_ebit_list_func(self):
        """
        :return:
        """
        revenue_list = [43185000000, 44048700000.0, 44929674000.0, 45828267480.0, 46744832829.6, 47679729486.192,\
                        48548454157.43041, 49346590743.77857, 50070011764.08236, 50714913515.60374, 51277849055.626945]
        margin_list = [0.07, 0.066, 0.064, 0.062, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06]
        result = ebit_list_func(revenue_list, margin_list)
        self.assertEqual(result, [3083409000.0000005, 2965358484.0, 2933009118.7200003, 2898179635.4351997,\
                                  2860783769.1715198, 2912907249.4458246, 2960795444.626714, 3004200705.8449416,\
                                  3042894810.936224, 3076670943.3376164])



if __name__ == '__main__':
    unittest.main()
