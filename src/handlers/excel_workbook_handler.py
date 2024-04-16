from utils.config import ConfigFileLocation, ExcelCellConfig
import openpyxl


class ExcelWorkbookHandler:
    def __init__(self):
        self.excel_file = openpyxl.load_workbook(
            ConfigFileLocation.get_excel_template_file_path,
            read_only=False,
            keep_vba=True,
        )

        self.selected_sheet = self.excel_file["Sheet1"]

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
                anCellID, fnCellID = ExcelCellConfig.get_attendance_dates_column_ids(
                    int(date)
                )
                self.selected_sheet[anCellID] = mark
                self.selected_sheet[fnCellID] = mark
