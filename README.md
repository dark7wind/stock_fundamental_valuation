# stock_fundamental_valuation
fundamental valuation

# Database: securities_database
1. **balance_sheet**
2. **cash_flow** 
3. **income_statement**
4. **income_statement_TTM** <br/>
The reason to add this table is that there only exists 4 quarterly income statement 
report. Thus we cannot use the 'trailling 12 months' to calculate the up-to-date 
financial data. 

5. **stock_info**
6. **stock_statistics**
7. **analysis_info_revenue**


# Update database table

# Multiple stocks evaluation

# Detail stock evaluation

# Process
1. Weekly update
* Wednesday update analysis info revenue 
* Wednesday update stock statistics
* Thursday update income_statement_TTM
    * run process/weekly/weekly_update_income_statement_TTM.py
* Friday update balance sheet
    * run process/weekly/weekly_update_balance_sheet.py
* Friday update cash flow
    * run process/weekly/weekly_update_cash_flow.py
* Friday update income_statement.py
    * run process/weekly/weekly_update_income_statement.py
* Friday update historical_price


2. Monthly update
* update stock info

3. yearly
* update industry 