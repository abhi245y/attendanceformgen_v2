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
                anCellID, fnCellID = ExcelCellConfig.get_an_fn_cell_id(int(date))
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
