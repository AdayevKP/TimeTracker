import datetime
import enum

from time_tracker.api import models


class StatsScale(enum.Enum):
    week = "week"


class StatsRequestApi(models.ApiBaseModel):
    scale: StatsScale


ProjectId = int
DayLabel = str


class StatsResponseApi(models.ApiBaseModel):
    total_time: datetime.timedelta
    time_per_project: dict[ProjectId, datetime.timedelta]
    time_per_day: dict[DayLabel, datetime.timedelta]
