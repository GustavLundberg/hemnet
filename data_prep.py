import pandas as pd
from webscraper import price_str_to_int
import re

df = pd.read_pickle('/py_scripts/df.pkl')
print(df)
print(df.info())
#print(df.dtypes())
print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')


# Applying some transformation on the columns to get them in the desired format
df['Antal rum'] = df['Antal rum'].apply(lambda x: str.split(x)[0])
df['Boarea'] = df['Boarea'].apply(lambda x: str.split(x)[0].replace(',', '.'))
df['Balkong'] = df['Balkong'] == 'Ja'
df['Förening'] = df['Förening'].apply(lambda x: re.sub('\n\nOm föreningen', '', x) if isinstance(x, str) else None)
df['Avgift'] = df['Avgift'].apply(price_str_to_int)
df['Driftkostnad'] = df['Driftkostnad'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
df['Kvadratmeterpris'] = df['Kvadratmeterpris'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
df['visits'] = df['visits'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
df['days_available'] = df['days_available'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
df['Uteplats'] = df['Uteplats'] == 'Ja'

print(df)