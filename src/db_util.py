import sqlite3

db_employee = sqlite3.connect("./src/database/main_db.sqlite")

cursor_employee = db_employee.cursor()


def get_employee_details(employee_name):
    res = cursor_employee.execute(
        """SELECT * FROM employee_details WHERE name=?""", (employee_name,)
    ).fetchone()
    db_employee.commit()
    return {
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


def get_employee_list():
    res = [
        "{0}".format(row[0])
        for row in cursor_employee.execute(
            """SELECT name FROM employee_details """
        ).fetchall()
    ]
    db_employee.commit()
    return res
