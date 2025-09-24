"""
"Viết một chương trình để tìm top n khách hàng có
tổng giá trị hóa đơn cao nhất từ cơ sở dữ liệu Chinook_Sqlite.sqlite,
với thông tin bao gồm CustomerId và TotalBilling, và hiển thị kết quả theo thứ tự giảm dần."
"""
import sqlite3
import pandas as pd

def query(n):
    try:
        sqliteConnection = sqlite3.connect('../../databases/Chinook_Sqlite.sqlite')
        cursor = sqliteConnection.cursor()
        print("DB Init")

        query = f"""    
        SELECT 
            CustomerId,
            SUM(Total) AS TotalBilling
        FROM Invoice
        GROUP BY CustomerId
        ORDER BY TotalBilling DESC
        LIMIT {n};
        """
        cursor.execute(query)

        # Lấy dữ liệu
        rows = cursor.fetchall()

        # Lấy tên cột từ cursor.description
        col_names = [desc[0] for desc in cursor.description]

        # Tạo DataFrame với tên cột
        df = pd.DataFrame(rows, columns=col_names)
        cursor.close()
    except sqlite3.Error as error:
        print("Error occured", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection closed")
    return df

pdss = query(7)
print(pdss)