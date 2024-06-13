import yaml
from utils.variable_storage import VariableStorage
import os


class ConfigFileLocation:
    def __init__(self):
        self.current_folder = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(self.current_folder))
        self.excel_cell_config = os.path.join(
            self.project_root, "config", "excel_cell_config.yaml"
        )
        self.other_templates = os.path.join(
            self.project_root, "config", "other_constants.yaml"
        )
        self.excel_template_file = os.path.join(
            self.project_root, "templates", "attendance_form_template.xlsm"
        )
        self.output = os.path.join(
            self.project_root,
            "output",
        )

        self.db_path = os.path.join(
            self.project_root, "src", "database", "main_db.sqlite"
        )

    def get_excel_cell_config_path(self):
        return self.excel_cell_config

    def get_certificate_template_path(self):
        return self.other_templates

    def get_excel_template_file_path(self):
        return self.excel_template_file

    def get_output_folder_path(self):
        return self.output

    def get_other_configs_path(self):
        return self.other_templates

    def get_db_path(self):
        return self.db_path


class OtherConfigs:
    def __init__(self):
        with open(ConfigFileLocation().get_other_configs_path(), "r") as file:
            self.config = yaml.safe_load(file)

    def get_wages(self, post):
        if post == "Messenger" or post == "Messenger-AD-A-8":
            return self.config["messengerPerDayWage"]
        elif post == "Labourer":
            return self.config["labourerPerDayWage"]
        elif post == "Driver":
            return self.config["driverPerDayWage"]
        elif post == "Buggy Operator":
            return self.config["buggyDriverPerDayWage"]

    def get_department(self):
        return self.config["department"]

    def get_db_path(self):
        return self.config["db_path"]

    def get_output_path(self, current_month, current_year, post):
        if post == "Messenger":
            return (
                self.config["output_save_path"]
                + f" {current_year}/"
                + f"/{current_month} {current_year}/"
                + self.config["contract_messengers_section"]
            )
        elif post == "Messenger-AD-A-8" or post == "Labourer":
            return (
                self.config["output_save_path"]
                + f" {current_year}/"
                + f"/{current_month} {current_year}/"
                + self.config["daily_wages_employee_section"]
            )
        elif post == "Buggy Operator":
            return self.config["output_save_path"] + f"/{current_month}/" + post


class ExcelCellConfig:
    def __init__(self):
        with open(ConfigFileLocation().get_excel_cell_config_path(), "r") as file:
            self.config = yaml.safe_load(file)

    def get_name_id(self):
        return self.config["name"]

    def get_department_id(self):
        return self.config["department"]

    def get_period_of_appointment_from_id(self):
        return self.config["periodOfAppointmentFrom"]

    def get_period_of_appointment_to_id(self):
        return self.config["periodOfAppointmentTo"]

    def get_period_of_extension_from_id(self):
        return self.config["periodofExtensionFrom"]

    def get_period_of_extension_to_id(self):
        return self.config["periodofExtensionTo"]

    def get_extension_prefix_sufix_id(self):
        return self.config["extensionPrefix"], self.config["extensionSufix"]

    def get_employeeid_id(self):
        return self.config["employeeID"]

    def get_employeeid_prefix_id(self):
        return self.config["employeeIDPrefix"]

    def get_bank_branch_id(self):
        return self.config["bankBranch"]

    def get_account_number_id(self):
        return self.config["accountNumber"]

    def get_ifsc_code_id(self):
        return self.config["ifscCode"]

    def get_mobile_number_id(self):
        return self.config["mobileNumber"]

    def get_first_half_column_id(self):
        return self.config["firstHalfColumn"]

    def get_second_half_column_id(self):
        return self.config["secondHalfColumn"]

    def get_main_certififcate_id(self):
        return self.config["mainCertififcate"]

    def get_holiday_certififcate_id(self):
        return self.config["holidayCertififcate"]

    def get_attendance_dates_column_ids(self, target):
        return self.config["dateColumnMapping"][target]

    def get_an_fn_cell_id_first_month(self, target):
        date_column_id = self.get_attendance_dates_column_ids(target=target)
        return date_column_id + self.config[
            "anRowNumberFirstMonth"
        ], date_column_id + self.config["fnRowNumberFirstMonth"]

    def get_an_fn_cell_id_second_month(self, target):
        date_column_id = self.get_attendance_dates_column_ids(target=target)
        return date_column_id + self.config[
            "anRowNumberSecondMonth"
        ], date_column_id + self.config["fnRowNumberSecondMonth"]


class CertificatesTemplate:
    def __init__(self):
        with open(ConfigFileLocation().get_certificate_template_path(), "r") as file:
            self.config = yaml.safe_load(file)

    def gender_pronoune(self, gender):
        if gender == "Male":
            pronoune_1 = "He"
            pronoune_2 = "his"
            return [pronoune_1, pronoune_2]
        else:
            pronoune_1 = "She"
            pronoune_2 = "her"
            return [pronoune_1, pronoune_2]

    def generate_main_certififcate(self, details: VariableStorage):
        return self.config["mainCertififcate"].format(
            details.employee_details.name,
            details.employee_details.post.replace("-AD-A-8", ""),
            OtherConfigs().get_department(),
            len(details.present_days),
            details.attendace_period_from,
            details.attendace_period_to,
            self.gender_pronoune(gender=details.employee_details.gender)[1],
            details.periodPerformance,
            self.gender_pronoune(gender=details.employee_details.gender)[0],
            details.remuneration,
            str(OtherConfigs().get_wages(details.employee_details.post)) + ".00/-",
            details.employee_details.post.replace("-AD-A-8", "").lower(),
        )

    def generate_holiday_certififcate(self, details: VariableStorage):
        return self.config["holidayCertificate"].format(
            self.gender_pronoune(gender=details.employee_details.gender)[0].lower(),
            details.holiday_duty_dates,
        )

    def generate_buggy_operator_certificate(self, details: VariableStorage):
        return self.config["buggyDriverCertificate"].format(
            details.employee_details.name,
            OtherConfigs().get_department(),
            len(details.present_days),
            details.attendace_period_from,
            details.attendace_period_to,
            details.periodPerformance,
            details.remuneration,
            str(OtherConfigs().get_wages(details.employee_details.post)) + ".00/-",
        )
