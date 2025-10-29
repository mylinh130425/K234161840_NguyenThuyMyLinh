import sys
import pickle
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow import Ui_MainWindow  # Đảm bảo tên file UI là MainWindow.py


# --- Tái tạo lớp FileUtil để tải mô hình ---
# Lưu ý: Nếu FileUtil.py có sẵn trong dự án, bạn có thể import trực tiếp.
class FileUtil:
    """Lớp tiện ích để tải/lưu mô hình Machine Learning."""

    @staticmethod
    def loadmodel(filename):
        try:
            # Sử dụng pickle để tải mô hình từ file nhị phân
            with open(filename, 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            print(f"Lỗi khi tải mô hình: {e}")
            return None


# ---------------------------------------------


class HousePricePredictor(QMainWindow):
    def __init__(self):
        super().__init__()
        # 1. Thiết lập giao diện người dùng
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 2. Tải mô hình ML (Thay thế 'housingmodel.zip' bằng tên file chính xác)
        self.trained_model = FileUtil.loadmodel("housingmodel.zip")
        if self.trained_model is None:
            QMessageBox.critical(self, "Lỗi Mô Hình",
                                 "Không thể tải mô hình 'housingmodel.zip'. Vui lòng kiểm tra file.")
            self.close()

        # 3. Kết nối sự kiện (Nút Prediction)
        # Tên nút là 'pushButton'
        self.ui.pushButton.clicked.connect(self.predict_house_price)

    def predict_house_price(self):
        try:
            # 4. Lấy dữ liệu từ QLineEdit và chuyển đổi sang float
            # Dựa trên tên Object Name trong Qt Designer (lineedit, lineedit_2, ...)

            # Avg. Area Income (lineEdit)
            income = float(self.ui.lineEdit.text())

            # Avg. Area House Age (lineEdit_2)
            house_age = float(self.ui.lineEdit_2.text())

            # Avg. Area Number of Rooms (lineEdit_3)
            num_rooms = float(self.ui.lineEdit_3.text())

            # Avg. Area Number of Bedrooms (lineEdit_4)
            num_bedrooms = float(self.ui.lineEdit_4.text())

            # Area Population (lineEdit_5)
            population = float(self.ui.lineEdit_5.text())

        except ValueError:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Vui lòng nhập giá trị số hợp lệ vào tất cả các trường.")
            # Xóa kết quả cũ nếu có lỗi
            self.ui.lineEdit_6.setText("")
            return

        # 5. Chạy dự đoán
        try:
            input_data = [[income, house_age, num_rooms, num_bedrooms, population]]

            # Thực hiện dự đoán
            prediction = self.trained_model.predict(input_data)[0]

            # Định dạng kết quả (ví dụ: làm tròn đến 2 chữ số thập phân)
            result_text = f"{prediction:,.2f}"  # Định dạng số có dấu phẩy phân cách

            # 6. Hiển thị kết quả (lineEdit_6)
            self.ui.lineEdit_6.setText(result_text)

        except Exception as e:
            QMessageBox.critical(self, "Lỗi Dự Đoán", f"Đã xảy ra lỗi trong quá trình chạy mô hình: {e}")
            self.ui.lineEdit_6.setText("Lỗi")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HousePricePredictor()
    window.show()
    sys.exit(app.exec())