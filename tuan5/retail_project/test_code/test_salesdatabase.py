from tuan5.retail_project.connectors.connector import Connector

conn=Connector(database="salesdatabase") #viết 1 thư viện nhưng có thể dùng hết mọi cơ sở dữ liêệu
conn.connect()
sql="select * from customer"
df=conn.queryDataset(sql)
print(df)
print(df.columns)