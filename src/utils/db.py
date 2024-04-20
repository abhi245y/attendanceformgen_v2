import sqlite3
from utils.config import ConfigFileLocation


class EmployeeDetails:
    def __init__(
        self,
        name,
        gender,
        post,
        employee_id,
        bank_name,
        ifsc_code,
        account_number,
        mobile_number,
        period_from,
        period_to,
    ):
        self.name = name
        self.gender = gender
        self.post = post
        self.employee_id = employee_id
        self.bank_name = bank_name
        self.ifsc_code = ifsc_code
        self.account_number = str(account_number)
        self.mobile_number = mobile_number
        self.appointment_period_from = period_from
        self.appointment_period_to = period_to


class JsonPayLoadStructure:
    def __init__(self, status, data):
        self.data = data
        self.status = status

    def get_payload(self):
        return {"status": self.status, "data": self.data}


class EmployeeDatabase:
    def __init__(self):
        self.db_path = ConfigFileLocation().get_db_path()
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_employee_details(self, employee_name, require_json=False):
        try:
            self.connect()
            self.cursor.execute(
                """SELECT * FROM employee_details WHERE name=?""", (employee_name,)
            )
            res = self.cursor.fetchone()
            self.close()
            if res:
                if require_json:
                    return res
                return EmployeeDetails(
                    name=res[0],
                    gender=res[1],
                    post=res[2],
                    employee_id=res[3],
                    bank_name=res[4],
                    ifsc_code=res[5],
                    account_number=res[6],
                    mobile_number=res[7],
                    period_from=res[8],
                    period_to=res[9],
                )
            else:
                print(f"Error No Details Found For: {employee_name}")
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving employee details: {e}")
            return JsonPayLoadStructure("Error retrieving employee details", None)

    def get_employee_list(self):
        try:
            self.cursor.execute("""SELECT name FROM employee_details""")
            res = [row[0] for row in self.cursor.fetchall()]
            return JsonPayLoadStructure("Sucess", res)
        except sqlite3.Error as e:
            print(f"Error retrieving employee list: {e}")
            return JsonPayLoadStructure("Error retrieving employee details", None)
