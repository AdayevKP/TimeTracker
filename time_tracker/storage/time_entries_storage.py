import dataclasses
import typing as tp

import fastapi as fa
import sqlalchemy as sa

from time_tracker.db import models as orm_models
from time_tracker.storage import common, exceptions, models, projects_storage


@dataclasses.dataclass
class TimeEntriesStorage(common.SAStorage):
    projects_storage: projects_storage.ProjectsStorageDep

    async def get_entry(self, entry_id: int) -> models.SavedTimeEntry | None:
        return await self.session.get(orm_models.TimeEntry, entry_id)

    async def save_entry(
        self, entry: models.TimeEntry
    ) -> models.SavedTimeEntry:
        if entry.project_id is not None:
            proj = await self.projects_storage.get_project(entry.project_id)
            if proj is None:
                raise exceptions.ProjectNotFound()

        new_entry = orm_models.TimeEntry(
            start_time=entry.start_time,
            end_time=entry.end_time,
            project_id=entry.project_id,
        )
        self.session.add(new_entry)
        await self.session.commit()
        await self.session.refresh(new_entry)
        return models.SavedTimeEntry.from_orm(new_entry)

    async def get_all_entries(
        self, offset: int | None, limit: int | None, project_id: int | None
    ) -> list[models.SavedTimeEntry]:
        if project_id is not None:
            proj = await self.projects_storage.get_project(project_id)
            if proj is None:
                raise exceptions.ProjectNotFound()

        query = sa.select(orm_models.TimeEntry).order_by(
            orm_models.TimeEntry.start_time
        )
        if project_id is not None:
            query = query.where(orm_models.TimeEntry.project_id == project_id)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = await self.session.execute(query)
        return [
            models.SavedTimeEntry.from_orm(r) for r in result.scalars().all()
        ]

    async def update_entry(
        self, entry_id: int, new_data: models.TimeEntry
    ) -> models.SavedTimeEntry | None:
        if new_data.project_id is not None:
            proj = await self.projects_storage.get_project(new_data.project_id)
            if proj is None:
                raise exceptions.ProjectNotFound()

        updated_entry = await self._update(
            orm_models.TimeEntry, entry_id, new_data
        )
        return updated_entry and models.SavedTimeEntry.from_orm(updated_entry)

    async def delete_entry(
        self, entry_id: int
    ) -> models.SavedTimeEntry | None:
        result = await self.session.execute(
            sa.delete(orm_models.TimeEntry)
            .where(orm_models.TimeEntry.id == entry_id)
            .returning(orm_models.TimeEntry)
        )
        deleted_entry = result.scalars().first()
        deleted_entry = deleted_entry and models.SavedTimeEntry.from_orm(
            deleted_entry
        )
        await self.session.commit()
        return deleted_entry


TimeEntriesStorageDep = tp.Annotated[TimeEntriesStorage, fa.Depends()]
