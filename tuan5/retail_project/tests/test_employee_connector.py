from retail_project.connectors.employee_connector import EmployeeConnector

ec = EmployeeConnector()
ec.connect()

em = ec.login(email="putin@hotmail.com", pwd="123")

if em == None:
    print("Login Failed!")
else:
    print("Login successful!")
    print(em)
