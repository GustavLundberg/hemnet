import pandas as pd

df = pd.read_pickle('/py_scripts/df.pkl')
print(df.head())

df['Antal rum'] = df['Antal rum'].apply(lambda x: str.split(x)[0])
df['Boarea'] = df['Boarea'].apply(lambda x: str.split(x)[0].replace(',', '.'))

print(df.head())