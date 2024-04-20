import datetime
import pandas


class DateTimeUtil:
    def __init__(self):
        pass

    def change_format(self, required_format, current_format, target_date):
        return datetime.datetime.strptime(target_date, current_format).strftime(
            required_format
        )

    def current_date(self, format):
        return datetime.datetime.now().strftime(format)

    def generate_dates(self, _from_date, _to_date):
        return [
            self.change_format("%d/%m/%Y", "%Y-%m-%d %H:%M:%S", str(date))
            for date in pandas.date_range(start=_from_date, end=_to_date)
        ]

    def get_day(self, target_date, current_format):
        return datetime.datetime.strptime(target_date, current_format).day

    def get_month(self, target_date, current_format):
        return datetime.datetime.strptime(target_date, current_format).strftime("%B")

    def get_year(self, target_date, current_format):
        return datetime.datetime.strptime(target_date, current_format).year
