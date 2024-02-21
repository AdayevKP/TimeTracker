import datetime

import pydantic


class Project(pydantic.BaseModel):
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class SavedProject(Project):
    id: int


class TimeEntry(pydantic.BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime | None = None
    project_id: int | None = None

    class Config:
        from_attributes = True

    @pydantic.field_validator("end_time", mode="after")
    @classmethod
    def _validate_end_time(
        cls, value: datetime.datetime, info: pydantic.ValidationInfo
    ) -> datetime.datetime:
        if value is not None and value < info.data["start_time"]:
            raise ValueError("end_time should be after start_time")

        return value


class SavedTimeEntry(TimeEntry):
    id: int
