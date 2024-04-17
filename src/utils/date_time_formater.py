import datetime


class DateTimeFormater:
    def __init__(self, target_date):
        self.target_date = target_date

    def change_format(self, required_format, current_format):
        return datetime.datetime.strptime(self.target_date, current_format).strftime(
            required_format
        )
