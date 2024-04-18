from utils.config import ExcelCellConfig, OtherConfigs, CertificatesTemplate
from utils.db import EmployeeDatabase
import openpyxl
from utils.variable_storage import VariableStorage


class ExcelWorkbookHandler:
    def __init__(self, template_file_path):
        self.excel_file = openpyxl.load_workbook(
            template_file_path,
            read_only=False,
            keep_vba=True,
        )

        self.selected_sheet = self.excel_file["Sheet1"]
        self.config = ExcelCellConfig
        self.employee_db = EmployeeDatabase()

    def mark_attendance(self, attendance_data):
        attendance_markings = {
            "present": "X",
            "absent": "A",
            "holiday": "H",
            "break": "B",
        }
        for attendance_type, attendance_dates in attendance_data.items():
            if attendance_dates is not None:
                mark = attendance_markings.get(attendance_type, "")
                for date in attendance_dates:
                    anCellID, fnCellID = self.config.get_an_fn_cell_id()(int(date))
                    self.selected_sheet[anCellID] = mark
                    self.selected_sheet[fnCellID] = mark

    def mark_irrelevant_dates(self, irrelevant_dates_list):
        line_char = "─"
        for date in irrelevant_dates_list:
            anCellID, fnCellID = ExcelCellConfig.get_attendance_dates_column_id()(
                int(date)
            )
            max_width_of_cell = max(
                len(str(self.selected_sheet[anCellID].value or "")),
                len(str(self.selected_sheet[fnCellID].value or "")),
            )
            line_string = line_char * max_width_of_cell

            self.selected_sheet[anCellID] = line_string
            self.selected_sheet[fnCellID] = line_string

    def fill_basic_info(self, details: VariableStorage):
        employee_details = self.employee_db.get_employee_details(
            details.current_employee_name
        )

        self.selected_sheet[self.config.get_first_half_column_id()] = (
            details.first_month_name
        )
        self.selected_sheet[self.config.get_second_half_column_id()] = (
            details.second_month_name
        )

        self.selected_sheet[self.config.get_department_id()] = (
            OtherConfigs.get_department()
        )
        self.selected_sheet[self.config.get_period_of_appointment_from_id()] = (
            employee_details.appointment_period_from
        )
        self.selected_sheet[self.config.get_period_of_appointment_to_id()] = (
            employee_details.appointment_period_to
        )
        self.selected_sheet[self.config.get_name_id()()] = details.name = (
            employee_details.name
        )

        if details.employee_id() != "n/a":
            self.selected_sheet[self.config.get_employeeid_prefix_id()] = "ID"
            self.selected_sheet[self.config.get_employeeid_id()] = (
                employee_details.employee_id
            )

        self.selected_sheet[self.config.get_bank_branch_id()] = details.mobile_number
        self.selected_sheet[self.config.get_account_number_id()] = (
            employee_details.account_number
        )
        self.selected_sheet[self.config.get_ifsc_code_id()] = employee_details.ifsc_code
        self.selected_sheet[self.config.get_mobile_number_id()] = (
            employee_details.mobile_number
        )

    def fill_main_certificates(self, details):
        self.selected_sheet[self.config.get_main_certififcate_id()] = (
            CertificatesTemplate.generate_main_certififcate(details)
        )

    def fill_holiday_certificates(self, details):
        self.selected_sheet[self.config.get_holiday_certififcate_id()] = (
            CertificatesTemplate.generate_holiday_certififcate(details)
        )

    def save(self, filePath):
        self.excel_file.save(filePath)
