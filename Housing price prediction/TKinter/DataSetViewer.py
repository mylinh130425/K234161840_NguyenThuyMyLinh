# DataSetViewer.py
from tkinter import *
from tkinter import ttk
import pandas as pd


class DataSetViewer:
    def __init__(self):
        pass

    def create_ui(self):
        self.root = Tk()
        self.root.title("Dataset viewer - House Pricing Prediction")
        self.root.geometry("800x600")

        main_panel = PanedWindow(self.root)
        main_panel["bg"] = "yellow"
        main_panel.pack(fill=BOTH, expand=True)

        # Định nghĩa các cột hiển thị trong Treeview
        columns = ('Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                   'Avg. Area Number of Bedrooms', 'Area Population', 'Price')

        # Tạo Treeview để hiển thị dữ liệu
        self.tree = ttk.Treeview(main_panel, columns=columns, show="headings")

        # Định nghĩa tiêu đề cho từng cột
        self.tree.heading("Avg. Area Income", text="Avg. Area Income")
        self.tree.heading("Avg. Area House Age", text="Avg. Area House Age")
        self.tree.heading("Avg. Area Number of Rooms", text="Avg. Area Number of Rooms")
        self.tree.heading("Avg. Area Number of Bedrooms", text="Avg. Area Number of Bedrooms")
        self.tree.heading("Area Population", text="Area Population")
        self.tree.heading("Price", text="Price")

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Thanh cuộn dọc
        scrollbar = ttk.Scrollbar(main_panel, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y, expand=True)

    def show_ui(self):
        self.root.mainloop()

    def show_data_listview(self, fileName):
        # Đọc dữ liệu từ file CSV
        df = pd.read_csv(fileName)

        # Chèn dữ liệu vào Treeview
        # Lưu ý: Code gốc có vẻ có lỗi logic ở vòng lặp,
        # nhưng tôi sẽ giữ nguyên cấu trúc vòng lặp như trong hình ảnh.
        for i in range(0, len(df)):
            # Lấy các giá trị cần hiển thị (0:Income, 1:Age, 2:Rooms, 3:Bedrooms, 4:Population, 5:Price)
            # Code gốc: df.iloc[1][...] nên sửa thành df.iloc[i][...] để hiển thị tất cả các hàng
            values = [df.iloc[i][0], df.iloc[i][1], df.iloc[i][2], df.iloc[i][3], df.iloc[i][4], df.iloc[i][5]]
            # In ra console (optional)
            # print(values)
            # Chèn hàng vào Treeview
            self.tree.insert('', END, values=values)