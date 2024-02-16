import dataclasses
import typing as tp

import fastapi as fa

from time_tracker.storage import projects_storage, time_entries_storage


@dataclasses.dataclass
class ApiContext:
    proj_storage: projects_storage.ProjectsStorageDep
    entries_storage: time_entries_storage.TimeEntriesStorageDep


ApiContextDep = tp.Annotated[ApiContext, fa.Depends()]
