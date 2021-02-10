import simfin as sf
import pandas as pd
pd.set_option('display.max_columns', None)

# Set your API-key for downloading data. This key gets the free data.
sf.set_api_key('free')

# Set the local directory where data-files are stored.
# The directory will be created if it does not already exist.
sf.set_data_dir('~/simfin_data/')

# Download the data from the SimFin server and load into a Pandas DataFrame.
df = sf.load_income(variant='annual', market='us')

# Print the first rows of the data.
print(df.head())
1