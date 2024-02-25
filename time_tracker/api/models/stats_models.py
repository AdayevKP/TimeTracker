import datetime
import enum
import typing as tp

import pydantic

from . import models


TimeDelta = tp.Annotated[
    datetime.timedelta,
    pydantic.PlainSerializer(lambda x: str(x), return_type=str),
]


class StatsScale(enum.Enum):
    week = "week"


class StatsRequestApi(models.ApiBaseModel):
    scale: StatsScale


class ProjectTime(models.ApiBaseModel):
    project_id: int | None
    time: TimeDelta


DayLabel = str


class StatsResponseApi(models.ApiBaseModel):
    total_time: TimeDelta
    time_per_day: dict[DayLabel, TimeDelta]
    time_per_project: list[ProjectTime]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "total_time": "5:33:02",
                    "time_per_day": {
                        "2024-02-19": "1:00:00",
                        "2024-02-20": "0:00:00",
                        "2024-02-21": "0:00:00",
                        "2024-02-22": "2:16:31",
                        "2024-02-23": "2:16:31",
                        "2024-02-24": "0:00:00",
                        "2024-02-25": "0:00:00",
                    },
                    "time_per_project": [
                        {"project_id": None, "time": "4:33:02"},
                        {"project_id": 1, "time": "1:00:00"},
                    ],
                }
            ]
        }
    }
