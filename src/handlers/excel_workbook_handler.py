from utils.config import ExcelCellConfig, OtherConfigs
import openpyxl


class ExcelWorkbookHandler:
    def __init__(self, template_file_path):
        self.excel_file = openpyxl.load_workbook(
            template_file_path,
            read_only=False,
            keep_vba=True,
        )

        self.selected_sheet = self.excel_file["Sheet1"]
        self.config = ExcelCellConfig

    def mark_attendance(self, attendance_data):
        attendance_markings = {
            "present": "X",
            "absent": "A",
            "holiday": "H",
            "break": "B",
            "quarantined": "Q",
        }
        for attendance_type, attendance_dates in attendance_data.items():
            mark = attendance_markings.get(attendance_type, "")
            for date in attendance_dates:
                anCellID, fnCellID = self.config.get_an_fn_cell_id(int(date))
                self.selected_sheet[anCellID] = mark
                self.selected_sheet[fnCellID] = mark

    def mark_irrelevant_dates(self, irrelevant_dates_list):
        line_char = "─"
        for date in irrelevant_dates_list:
            anCellID, fnCellID = ExcelCellConfig.get_attendance_dates_column_ids(
                int(date)
            )
            max_width_of_cell = max(
                len(str(self.selected_sheet[anCellID].value or "")),
                len(str(self.selected_sheet[fnCellID].value or "")),
            )
            line_string = line_char * max_width_of_cell

            self.selected_sheet[anCellID] = line_string
            self.selected_sheet[fnCellID] = line_string

    def fill_basic_info(self, details):
        self.selected_sheet[self.config.get_department_id] = (
            OtherConfigs.get_department()
        )
        self.selected_sheet[self.config.get_period_of_appointment_from_id] = (
            details.appointment_period_from
        )
        self.selected_sheet[self.config.get_period_of_appointment_to_id] = (
            details.appointment_period_to
        )
        self.selected_sheet[self.config.get_name_id()] = details.name = details.name
        if details.employee_id != "n/a":
            self.selected_sheet[self.config.get_employeeid_id] = details.employee_id

        self.selected_sheet[self.config.get_bank_branch_id] = details.mobile_number
        self.selected_sheet[self.config.get_account_number_id] = details.account_number
        self.selected_sheet[self.config.get_ifsc_code_id] = details.ifsc_code
        self.selected_sheet[self.config.get_mobile_number_id] = details.mobilenumber
