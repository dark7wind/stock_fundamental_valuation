import pandas as pd
import numpy as np
import datetime
from definitions import INDUSTRY_DIR
pd.set_option('display.max_columns', None)

file_name = '20210101_Industry_Global.csv'
df = pd.read_csv(INDUSTRY_DIR+file_name)
# clean the column names
df.columns = df.columns.str.replace(' ', '')
df.columns = df.columns.str.replace('-', '')
df.columns = df.columns.str.replace("[/,@,&,%,-,(,)]", "", regex=True)

# createDate and lastUpdatedDate
now = datetime.datetime.utcnow()
df['CreatedDate'] = now
df['LastUpdatedDate'] = now

# Date
date = file_name[0:8]
date = datetime.datetime.strptime(date, '%Y%m%d')
df['Date'] = date

# region
if 'Global' in file_name:
    df['Region'] = 'Global'
elif 'US' in file_name:
    df['Region'] = 'US'



# covert nan to 0
df = df.replace(np.nan, 'empty')

# create req strings
table_name = 'historical_price'
columns = ','.join(df.columns.values)
values = ("%s, " * len(df.columns))[:-2]
req = """INSERT IGNORE INTO %s (%s) VALUES (%s)""" % (table_name, columns, values)


# # insert MySQL
# mysql_cursor = db.cursor()
# chunk_size = 1000
# for i in range(0, len(df.index), chunk_size):
#     chunk_df = df.iloc[i: i + chunk_size]
#     data = [tuple(x) for x in chunk_df.values.tolist()]
#     mysql_cursor.executemany(req, data)
#     db.commit()
#
# mysql_cursor.close()
1