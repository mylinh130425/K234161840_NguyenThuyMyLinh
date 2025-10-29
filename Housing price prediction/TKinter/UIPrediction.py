# UIPrediction.py

from tkinter import *
from tkinter import messagebox, ttk
from tkinter.font import Font
from tkinter import filedialog as fd  # Đã đổi sfd thành fd để khớp với lệnh gọi sau
# from DataSetViewer import DataSetViewer # Cần đảm bảo file này tồn tại
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LinearRegression  # Thêm thư viện LinearRegression bị thiếu


# from FileUtil import FileUtil # Cần đảm bảo file này tồn tại

class UIPrediction:
    # Khai báo các biến thành viên (fields)
    fileName = ""  # Sử dụng cho biến tự chọn dataset

    # Các biến để lưu DataFrame và Model
    df = None
    X = None
    y = None
    X_train = None
    X_test = None
    y_train = None
    y_test = None
    lm = None
    coeff_df = None

    # --- Constructor ---
    def __init__(self):
        pass

    # --- Phương thức tạo giao diện ---
    def create_ui(self):
        self.root = Tk()
        self.root.title("House Pricing Prediction - Faculty of Information Systems")
        self.root.geometry("1500x850")

        # Main Panel
        main_panel = PanedWindow(self.root)
        main_panel["bg"] = "yellow"
        main_panel.pack(fill=BOTH, expand=True)

        # Top Panel (Title)
        top_panel = PanedWindow(main_panel, height=80)
        top_panel["bg"] = "blue"
        main_panel.add(top_panel)
        top_panel.pack(fill=X, side=TOP, expand=False)

        font = Font(family="tahoma", size=18)
        title_label = Label(top_panel, text='House Pricing Prediction', font=font)
        title_label["bg"] = "yellow"
        top_panel.add(title_label)

        # Center Panel
        center_panel = PanedWindow(main_panel)
        main_panel.add(center_panel)
        center_panel["bg"] = "pink"
        center_panel.pack(fill=BOTH, expand=True)

        # Choose Dataset Panel
        choose_dataset_panel = PanedWindow(center_panel, height=30)
        center_panel.add(choose_dataset_panel)
        choose_dataset_panel["bg"] = "orange"
        choose_dataset_panel.pack(fill=X)

        dataset_label = Label(choose_dataset_panel, text="Select Dataset:")
        self.selectedFileName = StringVar()
        self.selectedFileName.set("dataset/USA_Housing.csv")
        self.choose_dateset_entry = Entry(choose_dataset_panel, textvariable=self.selectedFileName)

        self.choose_dataset_button = Button(choose_dataset_panel, text="1.Pick Dataset",
                                            width=10, command=self.do_pick_data)
        self.view_dataset_button = Button(choose_dataset_panel, text="2.View Dataset", width=29,
                                          command=self.do_view_dataset)

        choose_dataset_panel.add(dataset_label)
        choose_dataset_panel.add(self.choose_dateset_entry)
        choose_dataset_panel.add(self.choose_dataset_button)
        choose_dataset_panel.add(self.view_dataset_button)
        self.view_dataset_button.pack(side=RIGHT, expand=False)
        self.choose_dataset_button.pack(side=RIGHT, expand=False)

        # Training Rate Panel
        training_rate_panel = PanedWindow(center_panel, height=30)
        center_panel.add(training_rate_panel)
        training_rate_panel.pack(fill=X)

        training_rate_label = Label(training_rate_panel, text="Training Rate:")
        self.training_rate = IntVar()
        self.training_rate.set(80)
        self.training_rate_entry = Entry(training_rate_panel, textvariable=self.training_rate, width=20)

        training_rate_panel.add(training_rate_label)
        training_rate_panel.add(self.training_rate_entry)

        percent_label = Label(training_rate_panel, text="%", width=20, anchor="e", justify=LEFT)  # Fix: "n" thành "%"
        percent_label.pack(side=RIGHT, expand=False, fill=X)  # Fix: fill=L=X] thành fill=X
        training_rate_panel.add(percent_label)

        self.train_model_button = Button(training_rate_panel, text="3.Train Model", width=28, command=self.do_train)
        training_rate_panel.add(self.train_model_button)

        self.evaluate_model_button = Button(training_rate_panel, text="4. Evaluate Model",
                                            width=28, command=self.do_evaluation)
        training_rate_panel.add(self.evaluate_model_button)

        self.status = StringVar()
        self.train_model_result_label = Label(training_rate_panel,
                                              textvariable=self.status)  # Fix: text=self.status.get()
        training_rate_panel.add(self.train_model_result_label)

        # Evaluate Panel (Table, Coefficient, Metrics)
        evaluate_panel = PanedWindow(center_panel, height=430)
        evaluate_panel["bg"] = "cyan"
        center_panel.add(evaluate_panel)
        evaluate_panel.pack(fill=X)

        table_evaluate_panel = PanedWindow(evaluate_panel, height=400)  # Fix height from 408 to 400
        evaluate_panel.add(table_evaluate_panel)

        # Định nghĩa cột cho Bảng kết quả Test Prediction
        columns = ('Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                   'Avg. Area Number of Bedrooms', 'Area Population', 'Original Price', 'Prediction Price')
        self.tree = ttk.Treeview(table_evaluate_panel, columns=columns, show="headings")

        # Cấu hình cột
        for col in columns:
            # Fix widths based on context (default width=128)
            self.tree.column(col, anchor=CENTER, stretch=NO, width=128)

            # Định nghĩa tiêu đề cột
        self.tree.heading("Avg. Area Income", text="Avg. Area Income")
        self.tree.heading("Avg. Area House Age", text="Avg. Area House Age")
        self.tree.heading("Avg. Area Number of Rooms", text="Avg. Area Number of Rooms")
        self.tree.heading("Avg. Area Number of Bedrooms", text="Avg. Area Number of Bedrooms")
        self.tree.heading("Area Population", text="Area Population")
        self.tree.heading("Original Price", text="Original Price")
        self.tree.heading("Prediction Price", text="Prediction Price")

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Thanh cuộn dọc
        scrollbar = ttk.Scrollbar(table_evaluate_panel, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y, expand=True)

        # Coefficient Panel (Bên phải bảng)
        coefficient_panel = PanedWindow(evaluate_panel)
        coefficient_panel["bg"] = "pink"
        coefficient_panel.pack(side=RIGHT, fill=X, expand=False)
        evaluate_panel.add(coefficient_panel)

        coefficient_detail_label = Label(coefficient_panel, text="Coefficient:")
        coefficient_panel.add(coefficient_detail_label)
        coefficient_detail_label.pack(side=TOP, fill=X, expand=False)

        coefficient_detail_panel = PanedWindow(coefficient_panel)
        coefficient_panel.add(coefficient_detail_panel)
        coefficient_detail_panel.pack(side=TOP, expand=False, fill=X)

        self.coefficient_detail_text = Text(coefficient_detail_panel, height=12, width=50)
        scroll = Scrollbar(coefficient_detail_panel)
        self.coefficient_detail_text.configure(yscrollcommand=scroll.set)
        self.coefficient_detail_text.pack(side=LEFT, expand=False, fill=X)

        scroll.config(command=self.coefficient_detail_text.yview)
        scroll.pack(side=RIGHT, fill=Y, expand=True)

        # Metric Panel (MAE, MSE, RMSE)
        metric_panel = PanedWindow(coefficient_panel, height=30)
        coefficient_panel.add(metric_panel)
        metric_panel.pack(side=TOP, fill=BOTH, expand=True)

        # MAE
        self.mae_value = DoubleVar()
        mae_label = Label(metric_panel, text="Mean Absolute Error (MAE):")
        mae_label.grid(row=0, column=0)
        mae_entry = Entry(metric_panel, width=20, textvariable=self.mae_value)
        mae_entry.grid(row=0, column=1)

        # MSE
        self.mse_value = DoubleVar()
        mse_label = Label(metric_panel, text="Mean Square Error (MSE):")
        mse_label.grid(row=1, column=0)
        mse_entry = Entry(metric_panel, width=20, textvariable=self.mse_value)
        mse_entry.grid(row=1, column=1)

        # RMSE
        self.rmse_value = DoubleVar()
        rmse_label = Label(metric_panel, text="Root Mean Square Error (RMSE):")
        rmse_label.grid(row=2, column=0)
        rmse_entry = Entry(metric_panel, width=20, textvariable=self.rmse_value)
        rmse_entry.grid(row=2, column=1)

        # Save Model Button
        savemodel_button = Button(metric_panel, text="5. Save Model", width=20, command=self.do_save_model)
        savemodel_button.grid(row=5, column=1)

        # Load Model Panel
        loadmodel_panel = PanedWindow(center_panel, height=26)
        loadmodel_panel["bg"] = "yellow"
        loadmodel_panel.pack(fill=BOTH, side=TOP)

        loadmodel_button = Button(loadmodel_panel, text="6. Load Model", command=self.do_load_model)
        loadmodel_button.grid(row=0, column=0)

        # Input Prediction Panel (Dự đoán đơn lẻ)
        input_prediction_panel = PanedWindow(center_panel)
        input_prediction_panel.pack(fill=BOTH, side=TOP, expand=True)

        # Avg. Area Income
        area_income_label = Label(input_prediction_panel, text="Avg. Area Income:")
        area_income_label.grid(row=0, column=0)
        self.area_income_value = DoubleVar()
        area_income_entry = Entry(input_prediction_panel, width=40, textvariable=self.area_income_value)
        area_income_entry.grid(row=0, column=1)

        # Avg. Area House Age
        area_house_age_label = Label(input_prediction_panel, text="Avg. Area House Age:")
        area_house_age_label.grid(row=1, column=0)
        self.area_house_age_value = DoubleVar()
        area_house_age_entry = Entry(input_prediction_panel, width=40, textvariable=self.area_house_age_value)
        area_house_age_entry.grid(row=1, column=1)

        # Avg. Area Number of Rooms
        area_number_of_rooms_label = Label(input_prediction_panel, text="Avg. Area Number of Rooms:")
        area_number_of_rooms_label.grid(row=2, column=0)
        self.area_number_of_rooms_value = DoubleVar()
        area_number_of_rooms_entry = Entry(input_prediction_panel, width=40,
                                           textvariable=self.area_number_of_rooms_value)
        area_number_of_rooms_entry.grid(row=2, column=1)

        # Avg. Area Number of Bedrooms
        area_number_of_bedrooms_label = Label(input_prediction_panel, text="Avg. Area Number of Bedrooms:")
        area_number_of_bedrooms_label.grid(row=3, column=0)
        self.area_number_of_bedrooms_value = DoubleVar()
        area_number_of_bedrooms_entry = Entry(input_prediction_panel, width=40,
                                              textvariable=self.area_number_of_bedrooms_value)  # Fix: Missing textvariable
        area_number_of_bedrooms_entry.grid(row=3, column=1)

        # Area Population
        area_population_label = Label(input_prediction_panel, text="Area Population:")
        area_population_label.grid(row=4, column=0)
        self.area_population_value = DoubleVar()
        area_population_entry = Entry(input_prediction_panel, width=40,
                                      textvariable=self.area_population_value)
        area_population_entry.grid(row=4, column=1)

        # Prediction Button
        prediction_button = Button(input_prediction_panel, text="7. Prediction House Pricing",
                                   command=self.do_prediction)
        prediction_button.grid(row=5, column=1)

        # Prediction Price Output
        prediction_price_label = Label(input_prediction_panel, text="Prediction Price:")
        prediction_price_label.grid(row=6, column=0)
        self.prediction_price_value = DoubleVar()
        prediction_price_entry = Entry(input_prediction_panel, width=40,
                                       textvariable=self.prediction_price_value)
        prediction_price_entry.grid(row=6, column=1)

        # Designed By Panel
        designedby_panel = PanedWindow(main_panel, height=26)
        designedby_panel["bg"] = "cyan"
        designedby_panel.pack(fill=BOTH, side=BOTTOM)

        designedby_label = Label(designedby_panel, text="Designed by: Tran Duy Thanh")
        designedby_label["bg"] = "cyan"
        designedby_label.pack(side=LEFT)

        # self.pass_placeholder = Label(designedby_panel, text="").pack() # Placeholder for line 222

    # --- Phương thức hiển thị giao diện ---
    def show_ui(self):
        self.root.mainloop()

    # --- Các hàm xử lý sự kiện ---

    def do_pick_data(self):
        # Sử dụng fd thay cho sfd trong hướng dẫn
        s = fd.askopenfilename(
            title="Choose dataset",
            initialdir="/",
            filetypes=(("Dataset CSV", "*.csv"), ("All Files", "*.*"))
        )
        self.selectedFileName.set(s)

    def do_view_dataset(self):
        # viewer = DataSetViewer() # Cần uncomment khi file DataSetViewer.py đã tồn tại
        # viewer.create_ui()
        # viewer.show_data_listview(self.selectedFileName.get())
        # viewer.show_ui()
        pass  # Giữ lại pass nếu chưa có DataSetViewer

    def do_train(self):
        # Lấy tỉ lệ train
        ratio = self.training_rate.get() / 100

        # Đọc dữ liệu
        self.df = pd.read_csv(self.selectedFileName.get())

        # Tách X và y (Feature Selection)
        self.X = self.df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                          'Avg. Area Number of Bedrooms', 'Area Population']]
        self.y = self.df['Price']

        # Chia tập Train/Test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=1 - ratio, random_state=101)

        # Huấn luyện mô hình Linear Regression
        self.lm = LinearRegression()
        self.lm.fit(self.X_train, self.y_train)

        self.status.set("Trained is finished")
        messagebox.showinfo("infor", "Trained is finished")

    def do_evaluation(self):
        # Kiểm tra mô hình đã được train chưa
        if self.lm is None:
            messagebox.showerror("Error", "Please train or load model first!")
            return

        # 1. Hiển thị Intercept
        print(self.lm.intercept_)
        insert_text = self.lm.intercept_

        # 2. Hiển thị Coefficients
        self.coeff_df = pd.DataFrame(self.lm.coef_, self.X.columns, columns=['Coefficient'])
        print(self.coeff_df)
        self.coefficient_detail_text.delete('1.0', END)  # Xóa nội dung cũ
        self.coefficient_detail_text.insert(END, self.coeff_df)

        # 3. Dự đoán và hiển thị kết quả TEST
        predictions = self.lm.predict(self.X_test)

        # Xóa nội dung bảng cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        y_test_array = np.asarray(self.y_test)
        # Chèn kết quả dự đoán vào bảng Treeview
        for i in range(0, len(self.X_test)):
            # Lấy các giá trị Feature và thêm giá trị thực/dự đoán
            values = [self.X_test.iloc[i][0], self.X_test.iloc[i][1], self.X_test.iloc[i][2], self.X_test.iloc[i][3],
                      self.X_test.iloc[i][4], y_test_array[i], predictions[i]]
            self.tree.insert('', END, values=values)

        # 4. Tính toán và hiển thị Metrics (MAE, MSE, RMSE)
        print('MAE:', metrics.mean_absolute_error(self.y_test, predictions))
        print('MSE:', metrics.mean_squared_error(self.y_test, predictions))
        print('RMSE:', np.sqrt(metrics.mean_squared_error(self.y_test, predictions)))

        self.mae_value.set(metrics.mean_absolute_error(self.y_test, predictions))
        self.mse_value.set(metrics.mean_squared_error(self.y_test, predictions))
        self.rmse_value.set(np.sqrt(metrics.mean_squared_error(self.y_test, predictions)))

        self.status.set("Evaluation is finished")
        messagebox.showinfo("infor", "Evaluation is finished")

    def do_save_model(self):
        # FileUtil.savemodel(self.lm, "housingmodel.zip") # Cần uncomment khi file FileUtil.py đã tồn tại
        # messagebox.showinfo("infor", "exported model to disk successful!")
        pass

    def do_load_model(self):
        # self.lm = FileUtil.loadmodel("housingmodel.zip") # Cần uncomment khi file FileUtil.py đã tồn tại
        # messagebox.showinfo("infor", "Loading model from disk successful!")
        pass

    def do_prediction(self):
        # Kiểm tra mô hình đã được load/train chưa
        if self.lm is None:
            messagebox.showerror("Error", "Please train or load model first!")
            return

        # Lấy các giá trị từ ô nhập liệu
        try:
            input_values = [
                self.area_income_value.get(),
                self.area_house_age_value.get(),
                self.area_number_of_rooms_value.get(),
                self.area_number_of_bedrooms_value.get(),
                self.area_population_value.get()
            ]

            # Chạy dự đoán
            result = self.lm.predict([input_values])
            self.prediction_price_value.set(result[0])

        except TclError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {e}")



# # Phần main.py
# if __name__ == '__main__':
#     ui = UIPrediction()
#     ui.create_ui()
#     ui.show_ui()