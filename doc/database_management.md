# Database Management

## Database
Database name: securities_database

### Tables overview
1. **balance_sheet**
2. **cash_flow** 
3. **income_statement**
4. **income_statement_TTM** (depreciated) 
5. **stock_statistics** 
6. **analysis_info_revenue**
7. **stock_info**
8. **industry**

### Table: balance_sheet

### Table: cash_flow

### Table: income_statement

### Table: income_statement_TTM (depreciated)
The reason to add this table is that there only exists 4 quarterly income statement report. Thus we cannot use the 'trailling 12 months' to calculate the up-to-date financial data.

### Table: stock_statistics

### Table: analysis_info_revenue

### Table: stock_info
This database is built based on the file `indname.xls` from Prof. Damodaran's webiste [Prof. Damodaran's webiste ](https://pages.stern.nyu.edu/~adamodar/) 'data breakdown' --> company lookup --> spreadsheet that includes the listing of industries and the companies in each one

**Action:** Check if the data is updated every six months
**Frequency:** 6 months

### Table: industry

###### to do 
######## Process to do
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


## MySQL
### Backup the database
In command terminal, run 
`sudo mysqldump [database name] > dumpfilename.sql` (dumpfilename --> backup_securities_database_20210927
)

### Restore the database
* Step 1: In mysql console, create a database `CREATE DATABASE [database name]`
* Step 2: In terminal, restore the database `sudo mysql -u root -p [database name] < dumpfilename.sql`
note: in windows (if cannot add the MySQL bin path to the windows system path environment), in Command Prompt `cd "c:\Program Files\MySQL\MySQL Server 8.0\bin"` and `mysql -u root -p [database name] < "c:\[dumpfile path]\dumpfilename.sql"`

### Delete Duplicate Records
In the table 'stock_statistics':
![database_remove_duplicates](assets/img/database_table_stock_statistics_PNR.PNG)
need to delete the duplicates on ticker and sharesOutstanding.
![database_remove_duplicates](assets/img/database_remove_duplicates_PNR.PNG)

MySQL syntax:
```sql
DELETE t1 FROM stock_statistics t1
INNER JOIN stock_statistics t2
    WHERE 
    t1.id < t2.id AND
    t1.ticker = t2.ticker AND
    t1.sharesOutstanding = t2.sharesOutstanding;
```

### Add (Composite) Unique Constraint
#### Show composite unique constraint
```sql
# check how you can create this table
SHOW CREATE TABLE stock_statistics;
```
#### Add composite unique constraint
```sql
ALTER TABLE `stock_statistics` ADD UNIQUE `unique_index_2`(`ticker`, `sharesOutstanding`);
```

