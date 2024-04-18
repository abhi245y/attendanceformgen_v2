from handlers.excel_workbook_handler import ExcelWorkbookHandler
from utils.db import EmployeeDatabase
from utils.variable_storage import VariableStorage
from utils.date_time_util import DateTimeUtil


class AttendanceFormGenerator:
    def __init__(
        self,
        absent_days,
        holidays_list,
        employee_name,
        is_present_on_holiday,
        holiday_duty_dates,
        break_date,
        attendance_period,
    ):
        self.absent_days = absent_days
        self.holidays_list = holidays_list
        self.employee_name = employee_name
        self.is_present_on_holiday = is_present_on_holiday
        self.holiday_duty_dates = holiday_duty_dates
        self.break_date = break_date
        self.attendance_period_from = attendance_period[0]
        self.attendance_period_to = attendance_period[1]
        self.excel_handler = ExcelWorkbookHandler()
        self.employee_db = EmployeeDatabase()
        self.employee_details = self.employee_db.get_employee_details(employee_name)
        self.var_store = VariableStorage()
        self.datetime_util = DateTimeUtil()

    def generate_present_dates(self):
        all_dates = self.datetime_util.generate_dates(
            self.attendance_period_from, self.attendance_period_to
        )

        filter_phase_1 = [date for date in all_dates if date not in self.absent_days]

        return [date for date in filter_phase_1 if date not in self.holidays_lists]

    def main(self):
        self.excel_handler.fill_basic_info(
            self.var_store(
                current_employee_name=self.employee_name,
                first_month_name=self.attendance_period_from,
                second_month_name=self.absent_days_to,
            )
        )
