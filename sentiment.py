import pandas as pd

df = pd.read_csv('data1.csv', on_bad_lines='skip')
print(df.head())
print(df.shape)
