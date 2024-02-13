import dataclasses
import fastapi as fa
import typing as tp

from time_tracker.storage import projects_storage
from time_tracker.storage import time_entries_storage


@dataclasses.dataclass
class ApiContext:
    proj_storage: projects_storage.ProjectsStorageDep
    entries_storage: time_entries_storage.TimeEntriesStorageDep


ApiContextDep = tp.Annotated[ApiContext, fa.Depends()]
