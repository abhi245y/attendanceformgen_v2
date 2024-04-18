import yaml


class ConfigFileLocation:
    def __init__(self):
        self.excel_cell_config = "config/excel_cell_config.yaml"
        self.other_templates = "config/other_templates.yaml"
        self.excel_template_file = "templates/attendance_form_template.xlsm"
        self.output = "output/"

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

    def get_an_fn_cell_id(self, target):
        date_column_id = self.get_attendance_dates_column_ids(target=target)
        return date_column_id + self.config[
            "anRowNumber"
        ], date_column_id + self.config["fnRowNumber"]


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

    def generate_main_certififcate(self, details):
        return self.config["mainCertififcate"].format(
            details.name,
            details.post,
            details.section_name,
            details.present_days,
            details.from_,
            details.to_,
            self.gender_pronoune[details.gender][1],
            details.periodPerformance,
            self.gender_pronoune[details.gender][0],
            details.remuneration,
            details.wage,
            details.post,
        )

    def generate_holiday_certififcate(self, details):
        return self.config["holidayCertificate"].format(
            self.gender_pronoune[details.gender][1], details.holiday_duty_dates
        )


class OtherConfigs:
    def __init__(self):
        with open(ConfigFileLocation().get_other_configs_path(), "r") as file:
            self.config = yaml.safe_load(file)

    def get_wages(self, post):
        if post == "Messenger":
            return self.config["messengerPerDayWage"]
        elif post == "Labourer":
            return self.config["labourerPerDayWage"]
        elif post == "Driver":
            return self.config["driverPerDayWage"]

    def get_department(self):
        return self.config["department"]

    def get_db_path(self):
        return self.config["db_path"]
