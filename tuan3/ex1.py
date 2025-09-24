"""
"Viết một chương trình Python để lọc các đơn hàng (OrderID) từ file CSV SalesTransactions.csv,
tính tổng giá trị của mỗi đơn hàng dựa trên UnitPrice, Quantity, và Discount,
và trả về danh sách các mã đơn hàng (OrderID) có tổng giá trị nằm trong khoảng
minValue đến maxValue do người dùng nhập, loại bỏ các giá trị trùng lặp."
"""
import pandas as pd

def find_orders_within_range(df, minValue, maxValue):
    # tổng giá trị từng đơn hàng
    order_totals = df.groupby('OrderID').apply(lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum())
    # lọc đơn hàng trong range
    orders_within_range = order_totals[(order_totals >= minValue) & (order_totals <= maxValue)]
    # danh sách các mã đơn hàng không trùng nhau
    unique_orders = df[df['OrderID'].isin(orders_within_range.index)]['OrderID'].drop_duplicates().tolist()

    return unique_orders

df = pd.read_csv('../datasets/SalesTransactions.csv')

minValue = float(input("Nhập giá trị min: "))
maxValue = float(input("Nhập giá trị max: "))
result = find_orders_within_range(df, minValue, maxValue)
print('Danh sách các hóa đơn trong phạm vi giá trị từ', minValue, 'đến', maxValue, ' là:', result)

