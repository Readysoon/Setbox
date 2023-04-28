from app.helpers.helpers import Helpers
from datetime import datetime, time

helpers = Helpers()


def test_make_string_into_date_and_make_a_list_of_week_days():
    date_string = "2023-04-28"
    date = helpers.make_string_into_date(date_string)
    assert date == datetime(2023, 4, 28)
    test_list = helpers.make_a_list_of_week_days(date)
    assert test_list == [
        "24.04.2023",
        "25.04.2023",
        "26.04.2023",
        "27.04.2023",
        "28.04.2023",
        "29.04.2023",
        "30.04.2023",
    ]


def test_round_time_to_next_hour_no_minutes_seconds():
    time_to_round = time(12, 0, 0)
    rounded_time = helpers.round_time_to_next_hour(time_to_round)
    assert rounded_time == time_to_round


def test_round_time_to_next_hour_with_minutes():
    time_to_round = time(12, 1, 0)
    rounded_time = helpers.round_time_to_next_hour(time_to_round)
    assert rounded_time != time_to_round
    assert rounded_time == time(13, 0, 0)


def test_round_time_to_next_hour_with_seconds():
    time_to_round = time(12, 0, 1)
    rounded_time = helpers.round_time_to_next_hour(time_to_round)
    assert rounded_time != time_to_round
    assert rounded_time == time(12, 0, 0)


def test_make_a_list_of_hours():
    start_time = time(9, 12, 1)
    end_time = time(15, 1, 59)
    test_list = helpers.make_a_list_of_hours(start_time, end_time)
    assert test_list == [
        time(9, 0, 0),
        time(10, 0, 0),
        time(11, 0, 0),
        time(12, 0, 0),
        time(13, 0, 0),
        time(14, 0, 0),
        time(15, 0, 0),
        time(16, 0, 0),
    ]


def test_make_a_list_of_hours_end_time_before_start_time():
    start_time = time(17, 1, 1)
    end_time = time(15, 1, 59)
    test_list = helpers.make_a_list_of_hours(start_time, end_time)
    assert test_list == []
