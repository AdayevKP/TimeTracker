import typing as tp

import fastapi as fa
import sqlalchemy as sa

from app.storage import common
from app.storage import models
from app.db import models as orm_models


class ProjectsStorage(common.SAStorage):
    async def get_project(self, proj_id: int) -> models.SavedProject | None:
        proj = await self.session.get(orm_models.Project, proj_id)
        return proj and models.SavedProject.from_orm(proj)

    async def save_project(self, proj: models.Project) -> models.SavedProject:
        new_project = orm_models.Project(
            name=proj.name,
            description=proj.description
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
        query = (
            sa.update(orm_models.Project)
            .returning(orm_models.Project)
            .where(orm_models.Project.id == proj_id)
            .values(new_data.dict(exclude_unset=True))
        )
        result = await self.session.execute(query)
        updated_proj = result.scalars().first()
        await self.session.commit()
        await self.session.refresh(updated_proj)

        return updated_proj and models.SavedProject.from_orm(updated_proj)


ProjectsStorageDep = tp.Annotated[ProjectsStorage, fa.Depends()]
