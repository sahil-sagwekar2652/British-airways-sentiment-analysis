import pandas as pd
import codecs

with codecs.open("data.csv", "r", "windows-1252") as f_in:
    with codecs.open("data1.csv", "w", "utf-8") as f_out:
        for line in f_in:
            f_out.write(line)

data = pd.read_csv('data1.csv', encoding='utf-8')
print(data.head())
