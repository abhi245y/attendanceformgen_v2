class VariableStorage:
    def __init__(
        self,
        current_employee_name=None,
        first_month_name=None,
        second_month_name=None,
        employee_details=None,
        present_days=None,
        attendace_period_from=None,
        attendace_period_to=None,
        periodPerformance=None,
        remuneration=None,
        holiday_duty_dates=None,
    ):
        self.current_employee_name = current_employee_name
        self.first_month_name = first_month_name
        self.second_month_name = second_month_name
        self.employee_details = employee_details
        self.present_days = present_days
        self.attendace_period_from = attendace_period_from
        self.attendace_period_to = attendace_period_to
        self.periodPerformance = periodPerformance
        self.remuneration = remuneration
        self.holiday_duty_dates = holiday_duty_dates
