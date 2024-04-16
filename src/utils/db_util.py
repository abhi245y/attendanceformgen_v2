import sqlite3


class JsonPayLoadStructure:
    def __init__(self, status, data):
        self.data = data
        self.status = status

    def get_payload(self):
        return {"status": self.status, "data": self.data}


class EmployeeDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def get_employee_details(self, employee_name):
        try:
            self.cursor.execute(
                """SELECT * FROM employee_details WHERE name=?""", (employee_name,)
            )
            res = self.cursor.fetchone()
            if res:
                payload = {
                    "name": res[0],
                    "gender": res[1],
                    "post": res[2],
                    "id": res[3],
                    "bank_name": res[4],
                    "ifsc_code": res[5],
                    "account_num": res[6],
                    "mobile_num": res[7],
                    "period_from": res[8],
                    "period_to": res[9],
                }
                return JsonPayLoadStructure("Sucess", payload)
            else:
                return JsonPayLoadStructure("Error no employee found", None)
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

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
