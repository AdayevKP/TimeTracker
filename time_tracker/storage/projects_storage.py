import typing as tp

import fastapi as fa
import sqlalchemy as sa

from time_tracker.storage import common
from time_tracker.storage import models
from time_tracker.db import models as orm_models


class ProjectsStorage(common.SAStorage):
    async def get_project(self, proj_id: int) -> models.SavedProject | None:
        proj = await self.session.get(orm_models.Project, proj_id)
        return proj and models.SavedProject.from_orm(proj)

    async def save_project(self, proj: models.Project) -> models.SavedProject:
        new_project = orm_models.Project(
            name=proj.name, description=proj.description
        )
        self.session.add(new_project)
        await self.session.commit()
        await self.session.refresh(new_project)

        return models.SavedProject.from_orm(new_project)

    async def get_all_projects(self) -> list[models.SavedProject]:
        result = await self.session.execute(sa.select(orm_models.Project))
        return [
            models.SavedProject.from_orm(r) for r in result.scalars().all()
        ]

    async def update_project(
        self, proj_id: int, new_data: models.Project
    ) -> models.SavedProject | None:
        updated_proj = await self._update(
            orm_models.Project, proj_id, new_data
        )
        return updated_proj and models.SavedProject.from_orm(updated_proj)


ProjectsStorageDep = tp.Annotated[ProjectsStorage, fa.Depends()]
