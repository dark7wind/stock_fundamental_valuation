# import sys
# sys.path.append('c:\\Users\\weiio\\Documents\\ds_project\\stock_fundamental_valuation')
import definitions

flag_cost_capital_terminal_override = False
flag_risk_free_terminal_override = False

if flag_cost_capital_terminal_override:
    cost_capital_terminal = 1
    print(cost_capital_terminal)
elif flag_risk_free_terminal_override:
    print(2)
else:
    print(3)
