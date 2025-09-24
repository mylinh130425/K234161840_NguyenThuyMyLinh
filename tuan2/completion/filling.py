from numpy import nan as NA
import pandas as pd

data = pd.DataFrame([[1., 6.5, 2.],
                     [1., NA, NA],
                     [NA, NA, NA],
                     [NA, 6.5, 1.]])
print(data)
print("-"*10)
cleaned=data.fillna(data.mean())
print(cleaned)
#Đa phần sẽ lấy trung bình hặc trung vị

