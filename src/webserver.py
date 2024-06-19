from flask import Flask, render_template, jsonify, request, redirect
from utils.db import EmployeeDatabase
from attendance_form_generator import AttendanceFormGenerator
from utils.date_time_util import DateTimeUtil

app = Flask(
    __name__,
    template_folder="web_template",
    static_url_path="/static",
)


emp_db = EmployeeDatabase()


def is_not_empty_or_whitespace(s):
    return bool(s.strip())


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
        employee_name = request.form.getlist("employee-name")[0]
        appointment_period_overide_check = (
            True if request.form.get("overide-check") else False
        )
        period_appointment_from = request.form.get("period-appointment-from")
        period_appointment_to = request.form.get("period-appointment-to")

        salary_period = [
            DateTimeUtil().change_format(
                "%d/%m/%Y", "%Y-%m-%d", request.form.get("salary-period-from")
            ),
            DateTimeUtil().change_format(
                "%d/%m/%Y", "%Y-%m-%d", request.form.get("salary-period-to")
            ),
        ]

        absent_days = []
        holiday_dates = []
        break_days = []
        irrelevant_dates_list = []
        holiday_duty_dates = []
        if is_not_empty_or_whitespace(request.form.get("absent-days")):
            print(request.form.get("absent-days"))
            absent_days.extend(request.form.get("absent-days").split(","))

        if is_not_empty_or_whitespace(request.form.get("holiday-dates")):
            holiday_dates.extend(
                request.form.get("holiday-dates").replace(" ", "").split(",")
            )

        if is_not_empty_or_whitespace(request.form.get("break-days")):
            break_days.extend(
                request.form.get("break-days").replace(" ", "").split(",")
            )

        if is_not_empty_or_whitespace(request.form.get("non-working-days")):
            irrelevant_dates_list.extend(
                request.form.get("non-working-days").replace(" ", "").split(",")
            )

        did_duty_on_holiday = (
            True if request.form.get("holiday-duty-certificate") else False
        )
        holiday_duty_dates = (
            request.form.get("holiday-duty-dates").replace(" ", "").split(",")
        )
        did_the_contract_extend = (
            True if request.form.get("new-contract-period") else False
        )

        if did_the_contract_extend:
            new_contract_period_from = request.form.get("new-contract-period-from")
            new_contract_period_to = request.form.get("new-contract-period-to")
        else:
            new_contract_period_from = []
            new_contract_period_to = []

        AttendanceFormGenerator(
            absent_days=absent_days,
            holidays_list=holiday_dates,
            employee_name=employee_name,
            did_duty_on_holiday=did_duty_on_holiday,
            holiday_duty_dates=holiday_duty_dates,
            break_date=break_days,
            attendance_period=salary_period,
            irrelevant_dates_list=irrelevant_dates_list,
            did_the_contract_extend=did_the_contract_extend,
            new_contract_period=[new_contract_period_from, new_contract_period_to],
        ).main()
        return redirect(request.referrer)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5005, host="0.0.0.0")
