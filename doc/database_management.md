## Backup MySQL
### backup the database
In command terminal, run 
`sudo mysqldump [database name] > dumpfilename.sql` (dumpfilename --> backup_securities_database_20210927
)

### restore the database
* Step 1: In mysql console, create a database `CREATE DATABASE [database name]`
* Step 2: In terminal, restore the database `sudo mysql -u root -p [database name] < dumpfilename.sql`
note: in windows (if cannot add the MySQL bin path to the windows system path environment), in Command Prompt `cd "c:\Program Files\MySQL\MySQL Server 8.0\bin"` and `mysql -u root -p [database name] < "c:\[dumpfile path]\dumpfilename.sql"`

## Delete Duplicate Records
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

## Add (Composite) Unique Constraint
### Show composite unique constraint
```sql
# check how you can create this table
SHOW CREATE TABLE stock_statistics;
```
### Add composite unique constraint
```sql
ALTER TABLE `stock_statistics` ADD UNIQUE `unique_index_2`(`ticker`, `sharesOutstanding`);
```

## Database Table Management
### Table: stock_info
This database is built based on the file `indname.xls` from Prof. Damodaran's webiste [Prof. Damodaran's webiste ](https://pages.stern.nyu.edu/~adamodar/) 'data breakdown' --> company lookup --> spreadsheet that includes the listing of industries and the companies in each one

**Action:** Check if the data is updated every six months
**Frequency:** 6 months