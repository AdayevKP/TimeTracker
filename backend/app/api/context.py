import dataclasses
import fastapi as fa
import typing as tp

from app.storage import projects_storage
from app.storage import time_entries_storage

ProjectStorageDep = tp.Annotated[projects_storage.ProjectsStorage, fa.Depends()]
TimeEntryStorageDep = tp.Annotated[time_entries_storage.TimeEntriesStorage, fa.Depends()]


@dataclasses.dataclass
class ApiContext:
    proj_storage: ProjectStorageDep
    entries_storage: TimeEntryStorageDep


ApiContextDep = tp.Annotated[ApiContext, fa.Depends()]
