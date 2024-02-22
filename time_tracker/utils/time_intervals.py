import datetime
import typing as tp


DatesScale = tp.Literal["week"]
DateBounds = tp.Tuple[datetime.date, datetime.date]


def _get_current_week_bounds() -> DateBounds:
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday())
    end = start + datetime.timedelta(days=6)
    return start, end


def _daterange(
    start_date: datetime.date, end_date: datetime.date
) -> tp.Generator[datetime.date, None, None]:
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + datetime.timedelta(n)


def get_date_bounds(scale: DatesScale) -> DateBounds:
    if scale == "week":
        return _get_current_week_bounds()

    raise ValueError(f"Unknown dates scale {scale}")


def get_all_dates_in_scale(scale: DatesScale) -> list[datetime.date]:
    if scale == "week":
        start, end = _get_current_week_bounds()
        return list(_daterange(start, end))

    raise ValueError(f"Unknown dates scale {scale}")
