import pytest
import datetime
from reminderbot.reminders import Reminder

def _make_ints(lst):
    return (int(s) for s in lst)

def _parse_time_strings(*args):
    return (datetime.time(*_make_ints(string.split(':'))) for string in args)

OFFHOURS_TEST_DATA = [
    ["23:00", "07:00", "22:00", False],
    ["23:00", "07:00", "01:59", True],
    ["23:00", "07:00", "06:59", True],
    ["23:00", "07:00", "07:59", False],
    ["03:00", "07:00", "07:59", False],
    ["13:00", "23:00", "13:59", True],
    ["13:00", "23:00", "23:30", False],
    ["23:00", "13:00", "15:59", False],
]

@pytest.mark.parametrize("start,end,current,expected", OFFHOURS_TEST_DATA)
def test_in_off_hours(start, end, current, expected):
    start, end, current = _parse_time_strings(start, end, current)
    rem = Reminder(1, "Test", "MSG", 1, None, 1, 1, start, end)
    assert rem.in_off_hours(current) == expected
