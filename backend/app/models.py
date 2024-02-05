from datetime import datetime

from pydantic import BaseModel


class Project(BaseModel):
    name: str
    description: str | None = None


class SavedProject(Project):
    id: int


class TimeEntry(BaseModel):
    start: datetime
    end: datetime | None
    project: Project | None


class SavedTimeEntry(TimeEntry):
    id: int
