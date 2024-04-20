from flask import Flask, render_template, jsonify
from utils.db import EmployeeDatabase

app = Flask(__name__, template_folder="template", static_url_path="/static")


emp_db = EmployeeDatabase()


@app.route("/get-employee-names")
def get_employee_names():
    return jsonify(emp_db.get_employee_list())


@app.route("/employee_details/<employee_name>")
def get_employee_details(employee_name):
    employee_details = emp_db.get_employee_details(employee_name=employee_name)

    if employee_details is None:
        return jsonify(error="Employee not found"), 404

    return jsonify(employee_details)

@app.route("/processing", methods=["GET", "POST"])
def processData():
    if request.method == "POST":
        

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5005)
