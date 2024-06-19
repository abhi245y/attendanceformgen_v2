from utils.config import ExcelCellConfig, OtherConfigs, CertificatesTemplate
from utils.db import EmployeeDatabase
import openpyxl
from utils.variable_storage import VariableStorage
from utils.date_time_util import DateTimeUtil


class ExcelWorkbookHandler:
    def __init__(self, template_file_path):
        self.excel_file = openpyxl.load_workbook(
            template_file_path,
            read_only=False,
            keep_vba=True,
        )

        self.selected_sheet = self.excel_file["Sheet1"]
        self.config = ExcelCellConfig()
        self.employee_db = EmployeeDatabase()
        self.dt_util = DateTimeUtil()

    def mark_attendance(self, attendance_data):
        attendance_markings = {
            "present": "X",
            "absent": "A",
            "holiday": "H",
            "break": "B",
        }
        for attendance_type, attendance_dates in attendance_data.items():
            # print(attendance_dates, attendance_type)
            if attendance_dates is not None or len(attendance_dates) != 0:
                mark = attendance_markings.get(attendance_type, "")
                for date in attendance_dates:
                    try:
                        day = self.dt_util.get_day(
                            target_date=date, current_format="%d/%m/%Y"
                        )
                        if day > 20:
                            anCellID, fnCellID = (
                                self.config.get_an_fn_cell_id_first_month(day)
                            )
                        else:
                            anCellID, fnCellID = (
                                self.config.get_an_fn_cell_id_second_month(day)
                            )
                        self.selected_sheet[anCellID] = mark
                        self.selected_sheet[fnCellID] = mark
                    except Exception as e:
                        print(f"Error in mark_attendance():{e}")
                        pass

    def mark_irrelevant_dates(self, irrelevant_dates_list):
        line_char = "-"
        for date in irrelevant_dates_list:
            try:
                day = self.dt_util.get_day(date, "%d/%m/%Y")
                if day > 20:
                    anCellID, fnCellID = self.config.get_an_fn_cell_id_first_month(day)
                else:
                    anCellID, fnCellID = self.config.get_an_fn_cell_id_second_month(day)
                max_width_of_cell = max(
                    len(str(self.selected_sheet[anCellID].value)),
                    len(str(self.selected_sheet[fnCellID].value)),
                )
                line_string = line_char * max_width_of_cell
                self.selected_sheet[anCellID] = line_string
                self.selected_sheet[fnCellID] = line_string
            except Exception as e:
                print(f"Error in mark_irrelevant_dates():{e}")
                pass

    def fill_basic_info(self, details: VariableStorage):
        self.selected_sheet[self.config.get_first_half_column_id()] = (
            details.first_month_name
        )

        self.selected_sheet[self.config.get_second_half_column_id()] = (
            details.second_month_name
        )

        self.selected_sheet[self.config.get_department_id()] = (
            OtherConfigs().get_department()
        )
        self.selected_sheet[self.config.get_period_of_appointment_from_id()] = (
            self.dt_util.change_format(
                target_date=details.employee_details.appointment_period_from,
                required_format="%d/%m/%Y",
                current_format="%Y-%m-%d",
            )
        )
        self.selected_sheet[self.config.get_period_of_appointment_to_id()] = (
            self.dt_util.change_format(
                target_date=details.employee_details.appointment_period_to,
                required_format="%d/%m/%Y",
                current_format="%Y-%m-%d",
            )
        )

        if details.did_the_contract_extend:
            extension_pre, extension_suf = self.config.get_extension_prefix_sufix_id()
            self.selected_sheet[extension_pre] = "Period Of Extension From:"
            self.selected_sheet[extension_suf] = "To:"

            self.selected_sheet[self.config.get_period_of_extension_from_id()] = (
                self.dt_util.change_format(
                    target_date=details.new_contract_period[0],
                    required_format="%d/%m/%Y",
                    current_format="%Y-%m-%d",
                )
            )
            self.selected_sheet[self.config.get_period_of_extension_to_id()] = (
                self.dt_util.change_format(
                    target_date=details.new_contract_period[1],
                    required_format="%d/%m/%Y",
                    current_format="%Y-%m-%d",
                )
            )

        self.selected_sheet[self.config.get_name_id()] = details.employee_details.name

        if details.employee_details.employee_id != "n/a":
            self.selected_sheet[self.config.get_employeeid_prefix_id()] = "ID:"
            self.selected_sheet[self.config.get_employeeid_id()] = (
                details.employee_details.employee_id
            )

        self.selected_sheet[self.config.get_bank_branch_id()] = (
            details.employee_details.bank_name
        )
        self.selected_sheet[self.config.get_account_number_id()] = (
            details.employee_details.account_number
        )
        self.selected_sheet[self.config.get_ifsc_code_id()] = (
            details.employee_details.ifsc_code
        )
        self.selected_sheet[self.config.get_mobile_number_id()] = (
            details.employee_details.mobile_number
        )

    def fill_main_certificates(self, details):
        self.selected_sheet[self.config.get_main_certififcate_id()] = (
            CertificatesTemplate().generate_main_certififcate(details=details)
        )

    def fill_buggy_operator_certificates(self, details):
        self.selected_sheet[self.config.get_main_certififcate_id()] = (
            CertificatesTemplate().generate_buggy_operator_certificate(details=details)
        )

    def fill_holiday_certificates(self, details):
        self.selected_sheet[self.config.get_holiday_certififcate_id()] = (
            CertificatesTemplate().generate_holiday_certififcate(details=details)
        )

    def save(self, filePath):
        self.excel_file.save(filePath)
