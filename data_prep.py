import pandas as pd
from webscraper import price_str_to_int
import re

# Applying transformations on the columns to get them in the desired format
# type = 'active' or 'sold'
def data_prep(df, type):

	if type == 'active':
		
		df['area'] = df['area'].apply(lambda x: 'Ön' if re.match('(\s|^)(Ön|ön).*', x) else x)
		df['area'] = df['area'].apply(lambda x: re.sub('(,|/|\(|\-).*$', '', x).strip())
		df['Antal rum'] = df['Antal rum'].apply(lambda x: str.split(x)[0])
		df['Boarea'] = df['Boarea'].apply(lambda x: float(str.split(x)[0].replace(',', '.')))
		df['Byggår'] = df['Byggår'].apply(lambda x: x if isinstance(x, str) else 2020)										# Assuming that property without Byggår is newly built
		df['Byggår'] = df['Byggår'].apply(lambda x: x.split('-')[-1] if isinstance(x, str) else x)							# Using the latest year as Byggår
		df['Balkong'] = df['Balkong'] == 'Ja'
		df['Förening'] = df['Förening'].apply(lambda x: re.sub('\n\nOm föreningen', '', x) if isinstance(x, str) else None)
		df['Avgift'] = df['Avgift'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
		df['Driftkostnad'] = df['Driftkostnad'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
		df['Kvadratmeterpris'] = df['Kvadratmeterpris'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
		df['visits'] = df['visits'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
		df['days_available'] = df['days_available'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
		df['avg_daily_visits'] = df.apply(lambda x: round(x['visits'] / max(1, x['days_available']), 2), axis = 1) 			# Feature engineering

		try:	
			f['Uteplats'] = df['Uteplats'] == 'Ja'

		except:
			print('[INFO] The column Uteplats does not exist')

	elif type == 'sold':

		df['size'] = df['size'].apply(lambda x: float(x.replace(',', '.')))

	return df

path = '/py_scripts/dataframes/df_Wed-Jul--8-14:40:42-2020.pkl'
path_sold = '/py_scripts/dataframes/df_sold_Wed-Jul--8-14:40:42-2020.pkl'





df = pd.read_pickle(path)
print(df.info(), '\n', df.head())

print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

df_sold = pd.read_pickle(path_sold)
print(df_sold.info(), '\n', df_sold.head())

print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

df = data_prep(df, type = 'active')
df_sold = data_prep(df_sold, type = 'sold')

print(df.info(), '\n', df.head())

print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

print(df_sold.info(), '\n', df_sold.head())

# Applying transformations to df_sold
#df_sold = pd.read_pickle('/py_scripts/dataframes/df_sold_Wed-Jul--8-14:13:59-2020.pkl')
#print(df_sold)
#df_sold['size'] = df_sold['size'].apply(lambda x: float(x.replace(',', '.')))
#print(df_sold)


#df.to_pickle('/py_scripts/dataframes/df_Wed-Jul--8-14:13:59-2020.pkl')
#df_sold.to_pickle('/py_scripts/dataframes/df_sold_Wed-Jul--8-14:13:59-2020.pkl')
