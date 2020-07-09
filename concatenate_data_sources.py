### Use to concatenate the data from multiple df_*.pkl's and df_sold_*.pkl

import requests
import pandas as pd
import time

from bs4 import BeautifulSoup

path = '/py_scripts/dataframes/df_Wed-Jul--8-14:40:42-2020.pkl'
path_sold = '/py_scripts/dataframes/df_sold_Wed-Jul--8-14:40:42-2020.pkl'

df = pd.read_pickle(path)
df_sold = pd.read_pickle(path_sold)
print(df.info(), '\n', df.head())
print('-----------------------------------------------------------------------------------')
print(df_sold.info(), '\n', df_sold.head())

# Testing the merging (DB-join) by manually adding a row into df_sold which has the location of that in another row in df
#d = {'location': 'Föreningsgatan 54C', 'size': 105.5, 'price': 999}
#df_sold = df_sold.append(d, ignore_index = True)


#print(df.info(), '\n', df.head())
#print(df_sold.info(), '\n', df_sold)

print('-----------------------------------------------------------------------------------')

# Concatenatinng one df with one df_sold
def concatenate_dfs(df, df_sold):

	return df.merge(df_sold, how = 'outer', left_on = ['address', 'Boarea'], right_on = ['location', 'size'])

# Concatenating two df's (active advertisements)
def concatenate_dfs_active(df1, df2):

	df1.merge(df2, )


#page = requests.get('https://www.hemnet.se/bostad/lagenhet-1rum-dockan-malmo-kommun-lovartsgatan-16931635')
#results = BeautifulSoup(page.content, 'html.parser')
#print(results)