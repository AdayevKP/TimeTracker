import dataclasses

from app.db import deps as db_deps


@dataclasses.dataclass
class SAStorage:
    session: db_deps.SessionDep
