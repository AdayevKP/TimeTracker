# mypy: ignore-errors
from dateutil import parser
import freezegun

from time_tracker.utils import time_intervals


@freezegun.freeze_time("2024-02-22")
def test_date_bounds():
    start, end = time_intervals.get_date_bounds(scale="week")
    assert start == parser.parse("2024-02-19").date()
    assert end == parser.parse("2024-02-25").date()


@freezegun.freeze_time("2024-02-22")
def test_all_dates_in_scale():
    res = time_intervals.get_all_dates_in_scale(scale="week")
    assert res == [
        parser.parse(d).date()
        for d in [
            "2024-02-19",
            "2024-02-20",
            "2024-02-21",
            "2024-02-22",
            "2024-02-23",
            "2024-02-24",
            "2024-02-25",
        ]
    ]
