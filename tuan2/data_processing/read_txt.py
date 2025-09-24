import pandas as pd

df = pd.read_csv("../../datasets/SalesTransactions.txt",
                 sep='\t',
                 encoding='utf-8',
                 dtype='unicode',
                 low_memory=False)

print(df)