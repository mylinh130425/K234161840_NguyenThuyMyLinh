"""
"Kết nối đến cơ sở dữ liệu Chinook_Sqlite.sqlite và truy vấn để
lấy 5 bản ghi đầu tiên từ bảng InvoiceLine, sau đó hiển thị kết quả dưới dạng DataFrame."
"""
import sqlite3
import pandas as pd

try:
    # Connect to DB and create a cursor
    sqliteConnection = sqlite3.connect('../../databases/Chinook_Sqlite.sqlite')
    cursor = sqliteConnection.cursor()
    print('DB Init :)')

    # Write a query and execute it with cursor
    query = "SELECT * FROM InvoiceLine LIMIT 5;"
    cursor.execute(query)

    # Fetch and output result
    df = pd.DataFrame(cursor.fetchall())
    print(df)

    # Close the cursor
    cursor.close()

except sqlite3.Error as error:
    print("sqlite3.Error as error: ", error)

# Close DB Connection irrespective of success or failure
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed :)')