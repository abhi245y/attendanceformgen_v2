from flask import Flask, render_template, jsonify, request, redirect
from utils.db import EmployeeDatabase


app = Flask(
    __name__,
    template_folder="web_template",
    static_url_path="/static",
)


emp_db = EmployeeDatabase()


@app.route("/get-employee-names")
def get_employee_names():
    res = emp_db.get_employee_list()
    if res["status"] == "Sucess":
        return jsonify(res["data"])


@app.route("/employee_details/<employee_name>")
def get_employee_details(employee_name):
    employee_details = emp_db.get_employee_details(
        employee_name=employee_name, require_json=True
    )

    if employee_details is None:
        return jsonify(error="Employee not found"), 404

    return jsonify(employee_details)


@app.route("/processing", methods=["GET", "POST"])
def processData():
    if request.method == "POST":
        employee_name = request.form.getlist("employee-name")
        appointment_period_overide_check = (
            True if request.form.get("overide-check") else False
        )
        print(type(appointment_period_overide_check))
        appointment_period_from = request.form.get("period-appointment-from")
        appointment_period_to = request.form.get("period-appointment-to")
        salary_period = [
            str(request.form.get("salary-period-from")),
            str(request.form.get("salary-period-to")),
        ]
        absent_days = request.form.get("absent-days").split(",")
        holiday_dates = request.form.get("holiday-dates").split(",")

        break_days = [request.form.get("break-days")]
        irrelevant_dates_list = request.form.get("non-working-days").split(",")
        did_duty_on_holiday = (
            True if request.form.get("holiday-duty-certificate") else False
        )
        holiday_duty_dates = request.form.get("holiday-duty-dates").split(",")

        print(
            employee_name,
            appointment_period_overide_check,
            appointment_period_from,
            appointment_period_to,
            salary_period,
            absent_days,
            holiday_dates,
            break_days,
            irrelevant_dates_list,
            did_duty_on_holiday,
            holiday_duty_dates,
        )
        return redirect(request.referrer)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5005)
