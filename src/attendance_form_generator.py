from handlers.excel_workbook_handler import ExcelWorkbookHandler
from utils.db import EmployeeDatabase
from utils.variable_storage import VariableStorage
from utils.date_time_util import DateTimeUtil
from utils.config import OtherConfigs, ConfigFileLocation
from utils.number_word_converter import NumberConverter
import os


class AttendanceFormGenerator:
    def __init__(
        self,
        absent_days,
        holidays_list,
        employee_name,
        did_duty_on_holiday,
        holiday_duty_dates,
        break_date,
        attendance_period,
        irrelevant_dates_list,
        did_the_contract_extend,
        new_contract_period,
    ):
        self.absent_days = absent_days
        self.holidays_list = holidays_list
        self.employee_name = employee_name
        self.did_duty_on_holiday = did_duty_on_holiday
        self.holiday_duty_dates = holiday_duty_dates
        self.break_date = break_date
        self.attendance_period_from = attendance_period[0]
        self.attendance_period_to = attendance_period[1]
        self.irrelevant_dates_list = irrelevant_dates_list
        self.excel_handler = ExcelWorkbookHandler(
            ConfigFileLocation().get_excel_template_file_path()
        )
        self.employee_db = EmployeeDatabase()
        self.employee_db.connect()
        self.employee_details = self.employee_db.get_employee_details(employee_name)
        self.datetime_util = DateTimeUtil()
        self.did_the_contract_extend = did_the_contract_extend
        self.new_contract_period = new_contract_period

    def generate_present_dates(self):
        all_dates = self.datetime_util.generate_dates(
            self.attendance_period_from, self.attendance_period_to
        )

        if self.did_duty_on_holiday:
            self.holidays_list = [
                date
                for date in self.holidays_list
                if date not in self.holiday_duty_dates
            ]

        filter_phase_1 = [date for date in all_dates if date not in self.absent_days]
        filter_phase_2 = [
            date for date in filter_phase_1 if date not in self.holidays_list
        ]
        filter_phase_3 = [
            date for date in filter_phase_2 if date not in self.irrelevant_dates_list
        ]
        return [date for date in filter_phase_3 if date not in self.break_date]

    def calculate_remuneration(self, present_days):
        amount = int(len(present_days)) * int(
            OtherConfigs().get_wages(self.employee_details.post)
        )
        in_words = NumberConverter().to_words(amount)

        return str(amount) + ".00/- (Rupees " + in_words + " Only )"

    def main(self):
        self.excel_handler.fill_basic_info(
            VariableStorage(
                current_employee_name=self.employee_name,
                employee_details=self.employee_details,
                first_month_name=" ".join(
                    [
                        self.datetime_util.get_month(
                            target_date=self.attendance_period_from,
                            current_format="%d/%m/%Y",
                        ),
                        str(
                            self.datetime_util.get_year(
                                target_date=self.attendance_period_from,
                                current_format="%d/%m/%Y",
                            )
                        ),
                    ]
                ),
                second_month_name=" ".join(
                    [
                        self.datetime_util.get_month(
                            target_date=self.attendance_period_to,
                            current_format="%d/%m/%Y",
                        ),
                        str(
                            self.datetime_util.get_year(
                                target_date=self.attendance_period_to,
                                current_format="%d/%m/%Y",
                            )
                        ),
                    ]
                ),
                did_the_contract_extend=self.did_the_contract_extend,
                new_contract_period=self.new_contract_period,
            )
        )
        if len(self.irrelevant_dates_list) != 0:
            self.excel_handler.mark_irrelevant_dates(self.irrelevant_dates_list)

        present_days = self.generate_present_dates()
        self.excel_handler.mark_attendance(
            attendance_data={
                "present": present_days,
                "absent": self.absent_days,
                "holiday": self.holidays_list,
                "break": self.break_date,
            }
        )

        if self.employee_details.post == "Buggy Operator":
            self.excel_handler.fill_buggy_operator_certificates(
                VariableStorage(
                    employee_details=self.employee_details,
                    present_days=present_days,
                    attendace_period_from=self.attendance_period_from,
                    attendace_period_to=self.attendance_period_to,
                    periodPerformance="satisfactory",
                    remuneration=self.calculate_remuneration(present_days=present_days),
                )
            )
            pass
        else:
            self.excel_handler.fill_main_certificates(
                VariableStorage(
                    employee_details=self.employee_details,
                    present_days=present_days,
                    attendace_period_from=self.attendance_period_from,
                    attendace_period_to=self.attendance_period_to,
                    periodPerformance="satisfactory",
                    remuneration=self.calculate_remuneration(present_days=present_days),
                )
            )

        if self.did_duty_on_holiday:
            self.excel_handler.fill_holiday_certificates(
                VariableStorage(
                    employee_details=self.employee_details,
                    holiday_duty_dates=", ".join(self.holiday_duty_dates),
                )
            )

        save_path = OtherConfigs().get_output_path(
            post=self.employee_details.post,
            current_month=" ".join(
                [
                    self.datetime_util.get_month(
                        target_date=self.attendance_period_to,
                        current_format="%d/%m/%Y",
                    ),
                    str(
                        self.datetime_util.get_year(
                            target_date=self.attendance_period_to,
                            current_format="%d/%m/%Y",
                        )
                    ),
                ]
            ),
        )
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            file_absolute_path = save_path + f"/{self.employee_name}" + ".xlsm"
        else:
            file_absolute_path = save_path + f"/{self.employee_name}" + ".xlsm"

        self.excel_handler.save(file_absolute_path)


# AttendanceFormGenerator(
#     absent_days=["01/04/2024"],
#     holidays_list=[
#         "24/03/2024",
#         "28/03/2024",
#         "29/03/2024",
#         "07/04/2024",
#         "10/04/2024",
#         "13/04/2024",
#         "14/04/2024",
#     ],
#     employee_name="Vinesh T",
#     did_duty_on_holiday=True,
#     holiday_duty_dates=["24/03/2024"],
#     break_date=[],
#     attendance_period=["21/03/2024", "20/04/2024"],
#     irrelevant_dates_list=["31/03/2024"],
# ).main()
