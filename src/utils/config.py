import yaml


class ConfigFileLocation:
    def __init__(self):
        self.excel_cell_config = "config/excel_cell_config.yaml"
        self.certificate_template = "config/certificate_template.yaml"
        self.excel_template_file = "templates/attendance_form_template.xlsm"
        self.output = "output/"

    def get_excel_cell_config_path(self):
        return self.excel_cell_config

    def get_certificate_template_path(self):
        return self.certificate_template

    def get_excel_template_file_path(self):
        return self.excel_template_file

    def get_output_folder_path(self):
        return self.output


class ExcelCellConfig:
    def __init__(self):
        with open(ConfigFileLocation().get_excel_cell_config_path(), "r") as file:
            self.config = yaml.safe_load(file)

    def get_name(self):
        return self.config["name"]

    def get_department(self):
        return self.config["department"]

    def get_period_of_appointment_from(self):
        return self.config["periodOfAppointmentFrom"]

    def get_period_of_appointment_to(self):
        return self.config["periodOfAppointmentTo"]

    def get_employee_id(self):
        return self.config["employeeID"]

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

    def get_quarantine_certififcate_id(self):
        return self.config["quarantineCertififcate"]

    def get_attendance_dates_column_ids(self, target):
        return self.config["dateColumnMapping"][target] + self.config[
            "anRowNumber"
        ], self.config["dateColumnMapping"][target] + self.config["fnRowNumber"]


class CertificatesTemplate:
    def __init__(self):
        with open(ConfigFileLocation().get_certificate_template_path(), "r") as file:
            self.config = yaml.safe_load(file)

    def generate_main_certififcate(self, details):
        return self.config["mainCertififcate"].format(
            details.name,
            details.post,
            details.section_name,
            details.present_days,
            details.from_,
            details.to_,
            details.gender,
            details.periodPerformance,
            details.gender,
            details.remuneration,
            details.wage,
            details.post,
        )

    def generate_holiday_certififcate(self, details):
        return self.config["holidayCertificate"].format(
            details.gender, details.holiday_duty_dates
        )

    def quarantine_certificate(self, details):
        return self.config["quarantineCertificate"].format(
            details.gender, details.quarantine_days, details.from_, details.to_
        )
