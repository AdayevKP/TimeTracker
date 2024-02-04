from datetime import datetime

from pydantic import BaseModel


class Project(BaseModel):
    name: str
    description: str | None = None


class TimeEntry(BaseModel):
    start: datetime
    end: datetime | None
    project: Project | None
