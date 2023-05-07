from datetime import datetime, time, timedelta
import filetype


class Helpers:
    def make_a_list_of_week_days(self, date):
        given_day_of_week = date.strftime("%w")
        if int(given_day_of_week) == 0:
            given_day_of_week = 7
        week_dates = []
        for day_of_week in range(1, 8):
            day = date + timedelta(days=-int(given_day_of_week) + day_of_week)
            day_string = day.strftime("%d.%m.%Y")
            week_dates.append(day_string)
        return week_dates

    def round_time(self, given_time):
        return given_time.replace(minute=0, second=0, microsecond=0)

    def round_time_to_next_hour(self, given_time):
        if given_time.replace(hour=0) > time(0, 0, 59):
            return self.round_time(given_time).replace(hour=given_time.hour + 1)
        return self.round_time(given_time)

    def make_a_list_of_hours(self, start_time, end_time):
        list_of_hours = []
        start_time_rounded = self.round_time(start_time)
        end_time_rounded = self.round_time_to_next_hour(end_time)
        hour_in_list = start_time_rounded
        while hour_in_list <= end_time_rounded:
            list_of_hours.append(hour_in_list)
            hour_in_list = hour_in_list.replace(hour=hour_in_list.hour + 1)
        return list_of_hours

    def get_file_type(self, filename):
        kind = filetype.guess("./files/" + filename)
        if kind is None:
            file_type = "Other"
        else:
            list_split = kind.mime.split(".")
            for a in list_split:
                b = a.split("/")
            file_type = b[-1]
        return file_type

    def make_string_into_date(self, date_string):
        return datetime.strptime(date_string, "%Y-%m-%d").date()
