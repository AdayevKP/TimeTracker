from datetime import datetime

from pydantic import BaseModel


class Project(BaseModel):
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class SavedProject(Project):
    id: int


class TimeEntry(BaseModel):
    start_time: datetime
    end_time: datetime | None = None
    project_id: int | None = None

    class Config:
        from_attributes = True


class SavedTimeEntry(TimeEntry):
    id: int
