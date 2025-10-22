from tuan5.retail_project.connectors.employee_connector import EmployeeConnector
from tuan5.retail_project.models.employee import Employee

ec = EmployeeConnector()
ec.connect()

emp = Employee()
emp.ID=7
emp.EmployeeCode = "EMP_K23416"
emp.Name = "K23416"
emp.Phone = "022795368"
emp.Email = "k23416@yahoo.com"
emp.Password = "456"
emp.IsDeleted = 0

result = ec.update_one_employee(emp)

if result > 0:
    print("Chúc mừng nha, đã thêm thành công")
else:
    print("Thật đáng thương")
