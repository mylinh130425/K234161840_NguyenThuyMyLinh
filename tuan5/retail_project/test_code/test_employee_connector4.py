from tuan5.retail_project.connectors.employee_connector import EmployeeConnector
from tuan5.retail_project.models.employee import Employee

ec = EmployeeConnector()
ec.connect()

emp = Employee()
emp.ID=8

result = ec.delete_one_employee(emp)

if result > 0:
    print("Chúc mừng nha, đã thêm thành công")
else:
    print("Thật đáng thương")
