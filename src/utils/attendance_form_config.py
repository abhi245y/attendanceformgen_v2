class AttendanceFormConfig:
    def __init__(
        self,
        employee_name,
        appointment_from,
        appointment_to,
        for_the_month_from,
        for_the_month_to,
        present_days,
        absent_days,
        holiday_dates,
        break_days,
        special_holiday_certificate,
        quarantine_certificate,
        special_holiday_present_dates,
        quarantined_dates,
        special_holiday_present_full_date,
        current_salary_period_from,
        current_salary_period_to,
        non_working_days,
        section_name,
    ):
        self.employee_name = employee_name
        self.appointment_from = appointment_from
        self.appointment_to = appointment_to
        self.for_the_month_from = for_the_month_from
        self.for_the_month_to = for_the_month_to
        self.present_days = present_days
        self.absent_days = absent_days
        self.holiday_dates = holiday_dates
        self.break_days = break_days
        self.special_holiday_certificate = special_holiday_certificate
        self.quarantine_certificate = quarantine_certificate
        self.special_holiday_present_dates = special_holiday_present_dates
        self.quarantined_dates = quarantined_dates
        self.special_holiday_present_full_date = special_holiday_present_full_date
        self.current_salary_period_from = current_salary_period_from
        self.current_salary_period_to = current_salary_period_to
        self.non_working_days = non_working_days
        self.section_name
