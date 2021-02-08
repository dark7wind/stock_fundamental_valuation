import unittest

from src.firm_input import growth_list_direct_func

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