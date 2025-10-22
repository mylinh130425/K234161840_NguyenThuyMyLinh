from PyQt6.QtWidgets import QMessageBox, QMainWindow

from tuan5.retail_project.connectors.employee_connector import EmployeeConnector
from tuan5.retail_project.uis.EmployeeMainWindow_ex import EmployeeMainWindowEx
from tuan5.retail_project.uis.LoginMainWindow import Ui_MainWindow


class LoginMainWindowEx(Ui_MainWindow):
    def __init__(self):
        pass

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButton_Login.clicked.connect(self.process_login)
    def process_login(self):
        email=self.lineEditEmail.text()
        pwd=self.lineEdit_Password.text()
        ec = EmployeeConnector()
        ec.connect()
        em = ec.login(email, pwd)
        if em == None:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Login Failed, please check your account again")
            msg.setWindowTitle("Login Failed")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
          self.gui_emp=EmployeeMainWindowEx()
          self.gui_emp.setupUi(QMainWindow())
          self.gui_emp.showWindow()
          self.MainWindow.close()