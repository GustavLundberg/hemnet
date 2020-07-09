### Use to concatenate the data from multiple df_*.pkl's and df_sold_*.pkl

import requests
import pandas as pd
import time
import os

from bs4 import BeautifulSoup

#path = '/py_scripts/dataframes/df_Wed-Jul--8-14:40:42-2020.pkl'
#path_sold = '/py_scripts/dataframes/df_sold_Wed-Jul--8-14:40:42-2020.pkl'

#df = pd.read_pickle(path)
#df_sold = pd.read_pickle(path_sold)

# Testing the merging (DB-join) by manually adding a row into df_sold which has the location of that in another row in df
#d = {'location': 'Föreningsgatan 54C', 'size': 105.5, 'price': 999}
#df_sold = df_sold.append(d, ignore_index = True)

# Concatenatinng one df with one df_sold
def merge_dfs(df, df_sold):

	return df.merge(df_sold, how = 'outer', left_on = ['address', 'Boarea'], right_on = ['location', 'size'])

# Concatenating two df's
def append_dfs(df1, df2):

	return df1.append(df2, ignore_index = True)


if __name__ == '__main__':

	path_dataframes = '/py_scripts/dataframes'

	df = None
	df_sold = None

	# Iterating over the files in path_dataframes, concatening the active ones to the active df, and the sold ones to the sold df
	for df_name in os.listdir(path_dataframes):
		
		df_temp = pd.read_pickle(f'{path_dataframes}/{df_name}')

		if 'df_sold' in df_name:

			if df_sold is None:
				df_sold = df_temp
			else:
				df_sold = append_dfs(df_sold, df_temp)

		elif 'df_' in df_name:

			if df is None:
				df = df_temp
			else:
				df = append_dfs(df, df_temp)

	# Removing duplicate rows
	df = df.drop_duplicates(subset = ['url', 'address', 'Boarea'])
	df_sold = df_sold.drop_duplicates(subset = ['location', 'size', 'price'])

	print(df.info(), '\n', df.head())
	print(df_sold.info(), '\n', df_sold.head())
