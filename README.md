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

3. Yearly update
* update industry 


# Git
1. Create issue xx at www.github.com
2. Create a branch in local repository <br>
`git checkout -b issxx`
3. When the issue is resolved, push the codes to the remote repository in www.github.com
4. In Github, click `Compare & pull request`, see example below:
![alt text](./readme/screenshot_compare_pull_request.png)
5. In Github, click `Create pull request`, base: `dev`, compare: `[branch]`
![alt text](./readme/screenshot_create_pull_request.png)
6. Click `merge pull request`
![alt text](./readme/screenshot_merge_pull_request.png)
7. Delete branch in Github
8. Close issue in Github
9. At local, switch to `dev` branch: `git checkout dev`
10. At local, pull from dev in Github: `git pull`
11. At local, delete the branch: `git branch -d iss56`
12. At local, create new branch according to the name of issue: `git checkout -b iss58`

# Git release new version
