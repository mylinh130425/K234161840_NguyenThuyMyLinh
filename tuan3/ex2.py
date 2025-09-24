"""
"Viết một chương trình Python để tìm top 3 sản phẩm có tổng giá trị bán ra (sold value)
cao nhất từ file CSV SalesTransactions.csv, với thông tin bao gồm Rank (thứ hạng),
ProductID (mã sản phẩm), và SoldValue (tổng giá trị bán ra),
và hiển thị kết quả theo thứ tự giảm dần."
"""
import pandas as pd

def top3_products_by_sales(df):
    # Tính sold value cho từng ProductID
    df['SoldValue'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

    product_sales = df.groupby('ProductID')['SoldValue'].sum()

    # Lấy top 3 sản phẩm có doanh thu cao nhất
    top3 = product_sales.sort_values(ascending=False).head(3).reset_index()

    top3.index = top3.index + 1
    top3.index.name = "Rank"

    return top3

# Đọc dữ liệu
df = pd.read_csv("../datasets/SalesTransactions.csv", sep=',')

# Tính top 3
result = top3_products_by_sales(df)
print("\nTop 3 sản phẩm có sold value cao nhất:")
print(result)
