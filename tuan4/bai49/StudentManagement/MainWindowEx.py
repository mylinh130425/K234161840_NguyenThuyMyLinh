# Bước 4.1: Coding kế thừa Ui_MainWindow, và định nghĩa các biến như bên dưới:
import base64
import traceback
import mysql.connector
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox
from MainWindow import Ui_MainWindow

class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.default_avatar = "images/ic_no_avatar.png"
        self.id = None
        self.code = None
        self.name = None
        self.age = None
        self.avatar = None
        self.intro = None
        self.conn = None  # Add connection attribute to store the database connection

    # Bước 4.2: Override phương thức setupUI: Hàm trên, ta thiết lập hàm nạp giao diện và khai báo các signals + slots
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.tableWidgetStudent_2.itemSelectionChanged.connect(self.processItemSelection)
        self.pushButtonAvatar_2.clicked.connect(self.pickAvatar)
        self.pushButtonRemoveAvatar_2.clicked.connect(self.removeAvatar)
        self.pushButtonInsert_2.clicked.connect(self.processInsert)
        self.pushButtonUpdate_2.clicked.connect(self.processUpdate)
        self.pushButtonRemove_2.clicked.connect(self.processRemove)

    def show(self):
        self.MainWindow.show()

    # Bước 4.3: Viết mã lệnh kết nối MySQL Server, cơ sở dữ liệu studentmanagement
    def connectMySQL(self):
        server = "localhost"
        port = 3306
        database = "studentmanagement"
        username = "root"
        password = "@Bb13042005"

        self.conn = mysql.connector.connect(
            host=server,
            port=port,
            database=database,
            user=username,
            password=password
        )

    # Bước 4.4: Viết lệnh truy vấn toàn bộ Student và hiển thị lên QTableWidget
    def selectAllStudent(self):
        cursor = self.conn.cursor()
        sql = "select * from student"
        cursor.execute(sql)
        dataset = cursor.fetchall()
        self.tableWidgetStudent_2.setRowCount(0)
        row = 0
        for item in dataset:
            row = self.tableWidgetStudent_2.rowCount()
            self.tableWidgetStudent_2.insertRow(row)

            self.id = item[0]
            self.code = item[1]
            self.name = item[2]
            self.age = item[3]
            self.avatar = item[4]
            self.intro = item[5]

            self.tableWidgetStudent_2.setItem(row, 0, QTableWidgetItem(str(self.id)))
            self.tableWidgetStudent_2.setItem(row, 1, QTableWidgetItem(self.code))
            self.tableWidgetStudent_2.setItem(row, 2, QTableWidgetItem(self.name))
            self.tableWidgetStudent_2.setItem(row, 3, QTableWidgetItem(str(self.age)))

        cursor.close()

    # Bước 4.5: Viết hàm hiển thị thông tin chi tiết student khi nhấn vào từng dòng dữ liệu trong QTableWidget
    def processItemSelection(self):
        row = self.tableWidgetStudent_2.currentRow()
        if row == -1:
            return
        try:
            code = self.tableWidgetStudent_2.item(row, 1).text()
            cursor = self.conn.cursor()
            sql = "select * from student where code=%s"
            val = (code,)
            cursor.execute(sql, val)
            item = cursor.fetchone()
            if item is not None:
                self.id = item[0]
                self.code = item[1]
                self.name = item[2]
                self.age = item[3]
                self.avatar = item[4]
                self.intro = item[5]
                self.lineEditId_2.setText(str(self.id))
                self.lineEditCode_2.setText(self.code)
                self.lineEditName_2.setText(self.name)
                self.lineEditAge_2.setText(str(self.age))
                self.lineEditIntro_2.setText(self.intro)
                if self.avatar is not None:
                    imgdata = base64.b64decode(self.avatar)
                    pixmap = QPixmap()
                    pixmap.loadFromData(imgdata)
                    self.labelAvatar_2.setPixmap(pixmap)
                else:
                    pixmap = QPixmap(self.default_avatar)
                    self.labelAvatar_2.setPixmap(pixmap)
            else:
                print("Not Found")
            cursor.close()
        except:
            traceback.print_exc()

    # Bước 4.6: Viết lệnh chọn Avatar và xóa Avatar, có tạo base64string
    def pickAvatar(self):
        filters = "Picture PNG (*.png);;All files(*)"
        filename, selected_filter = QFileDialog.getOpenFileName(
            self.MainWindow,
            filter=filters,
        )
        if filename == '':
            return
        pixmap = QPixmap(filename)
        self.labelAvatar_2.setPixmap(pixmap)

        with open(filename, "rb") as image_file:
            self.avatar = base64.b64encode(image_file.read())
            print(self.avatar)

    def removeAvatar(self):
        self.avatar = None
        pixmap = QPixmap(self.default_avatar)
        self.labelAvatar_2.setPixmap(pixmap)

    # Bước 4.7: Viết hàm thêm mới Student
    def processInsert(self):
        try:
            cursor = self.conn.cursor()
            sql = "insert into student(Code,Name,Age,Avatar,Intro) values(%s,%s,%s,%s,%s)"

            self.code = self.lineEditCode_2.text()
            self.name = self.lineEditName_2.text()
            self.age = int(self.lineEditAge_2.text())
            if not hasattr(self, 'avatar'):
                self.avatar = None
            self.intro = self.lineEditIntro_2.text()
            val = (self.code, self.name, self.age, self.avatar, self.intro)

            cursor.execute(sql, val)
            self.conn.commit()

            print(cursor.rowcount, " record inserted")
            self.lineEditId_2.setText(str(cursor.lastrowid))

            cursor.close()
            self.selectAllStudent()
        except:
            traceback.print_exc()

    # Bước 4.8: Viết hàm cập nhật Student
    def processUpdate(self):
        cursor = self.conn.cursor()
        sql = "update student set Code=%s,Name=%s,Age=%s,Avatar=%s,Intro=%s where Id=%s"
        self.id = int(self.lineEditId_2.text())
        self.code = self.lineEditCode_2.text()
        self.name = self.lineEditName_2.text()
        self.age = int(self.lineEditAge_2.text())
        if not hasattr(self, 'avatar'):
            self.avatar = None
        self.intro = self.lineEditIntro_2.text()

        val = (self.code, self.name, self.age, self.avatar, self.intro, self.id)

        cursor.execute(sql, val)
        self.conn.commit()

        print(cursor.rowcount, " record updated")
        cursor.close()
        self.selectAllStudent()

    # Bước 4.9: Viết hàm xóa Student
    def processRemove(self):
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Confirmation Deleting")
        dlg.setText("Are you sure you want to delete?")
        dlg.setIcon(QMessageBox.Icon.Question)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        dlg.setStandardButtons(buttons)
        button = dlg.exec()
        if button == QMessageBox.StandardButton.No:
            return
        cursor = self.conn.cursor()
        sql = "delete from student where Id=%s"
        val = (self.lineEditId_2.text(),)

        cursor.execute(sql, val)
        self.conn.commit()

        print(cursor.rowcount, " record removed")
        cursor.close()
        self.selectAllStudent()
        self.clearData()

    # Bước 4.10: Viết hàm xóa dữ liệu trên giao diện của phần chi tiết
    def clearData(self):
        self.lineEditId_2.setText("")
        self.lineEditCode_2.setText("")
        self.lineEditName_2.setText("")
        self.lineEditAge_2.setText("")
        self.lineEditIntro_2.setText("")
        self.avatar = None