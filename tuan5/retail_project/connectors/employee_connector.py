from retail_project.connectors.connector import Connector
from retail_project.models.employee import Employee

class EmployeeConnector(Connector):
    def login(self, email, pwd):
        sql = "SELECT * FROM employee " \
              "WHERE Email=%s AND Password=%s"
        val = (email, pwd)
        dataset = self.fetchone(sql, val)

        if dataset == None:
            return None

        emp = Employee(
            dataset[0],  # ID
            dataset[1],  # EmployeeCode
            dataset[2],  # Name
            dataset[3],  # Phone
            dataset[4],  # Email
            dataset[5],  # Password
            dataset[6]   # IsDeleted
        )

        return emp
