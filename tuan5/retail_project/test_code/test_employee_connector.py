#from retail_project.connectors.employee_connector import EmployeeConnector
from tuan5.retail_project.connectors.employee_connector import EmployeeConnector

ec = EmployeeConnector()
ec.connect()

em = ec.login(email="putin@gmail.com", pwd="456")

if em == None:
    print("Login Failed!")
else:
    print("Login successful!")
    print(em)

#test get all employee
print("List of Employee:")
ds=ec.get_all_employee()
print(ds)
for emp in ds:
    print(emp)
id=30
emp=ec.get_detail_infor(id)
if emp==None:
    print("Không có nhân viên nào có mã = ",id)
else:
    print("Tìm thấy nhân viên có mã =", id)
    print(emp)