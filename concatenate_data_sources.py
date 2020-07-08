### Use to concatenate the data from df.pkl and df_sold.pkl

import pandas as pd
import time

path = '/py_scripts/dataframes/df_Wed-Jul--8-14:13:59-2020.pkl'
path_sold = '/py_scripts/dataframes/df_sold_Wed-Jul--8-14:13:59-2020.pkl'

df = pd.read_pickle(path)
df_sold = pd.read_pickle(path_sold)

# Testing the merging (DB-join) by manually adding a row into df_sold which has the location of that in another row in df
d = {'location': 'Föreningsgatan 54C', 'size': 105.5, 'price': 999}
df_sold = df_sold.append(d, ignore_index = True)


#print(df.info(), '\n', df.head())
#print(df_sold.info(), '\n', df_sold)

print('-----------------------------------------------------------------------------------')

def concatenate_dfs(df, df_sold):

	conc = df.merge(df_sold, how = 'outer', left_on = ['address', 'Boarea'], right_on = ['location', 'size'])
	print(conc)

	return

res = concatenate_dfs(df, df_sold)
#print(res)

t = time.asctime()
t = t.replace(' ', '-')
print(type(t), t)