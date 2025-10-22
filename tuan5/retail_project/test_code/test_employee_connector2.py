from tuan5.retail_project.connectors.employee_connector import EmployeeConnector
from tuan5.retail_project.models.employee import Employee

ec = EmployeeConnector()
ec.connect()

emp = Employee()
emp.EmployeeCode = "EMP888"
emp.Name = "Doremon"
emp.Phone = "113"
emp.Email = "doremon@yahoo.com"
emp.Password = "456"
emp.IsDeleted = 0

result = ec.insert_one_employee(emp)

if result > 0:
    print("Chúc mừng nha, đã thêm thành công")
else:
    print("Thật đáng thương")
