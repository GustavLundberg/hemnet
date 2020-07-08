### Use to concatenate the data from df.pkl and df_sell.pkl

import pandas as pd

path = '/py_scripts/df.pkl'
path_sell = '/py_scripts/df_sell.pkl'

df = pd.read_pickle(path)
df_sell = pd.read_pickle(path_sell)

# Testing the merging (DB-join) by manually adding a row into df_sell which has the location of that in another row in df
d = {'location': 'Föreningsgatan 54C', 'size': 105.5, 'price': 999}
df_sell = df_sell.append(d, ignore_index = True)


#print(df.info(), '\n', df.head())
#print(df_sell.info(), '\n', df_sell)

print('-----------------------------------------------------------------------------------')

def concatenate_dfs(df, df_sell):

	conc = df.merge(df_sell, how = 'outer', left_on = ['address', 'Boarea'], right_on = ['location', 'size'])
	print(conc)

	return

res = concatenate_dfs(df, df_sell)
#print(res)
