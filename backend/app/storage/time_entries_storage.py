import datetime

from app.storage import exceptions, models
from app.storage import projects_storage


class TimeEntriesStorage:
    _CUR_ID = 5
    _ENTRIES = {
        1: models.SavedTimeEntry(
            id=1,
            start_time=datetime.datetime.strptime('2024-01-13 12:30', "%Y-%m-%d %H:%M")
        ),
        2: models.SavedTimeEntry(
            id=2,
            start_time=datetime.datetime.strptime('2024-01-13 12:30', "%Y-%m-%d %H:%M"),
            end_time=datetime.datetime.strptime('2024-01-13 12:40', "%Y-%m-%d %H:%M"),
            project_id=2
        ),
        3: models.SavedTimeEntry(
            id=3,
            start_time=datetime.datetime.strptime('2024-01-13 22:30', "%Y-%m-%d %H:%M"),
            end_time=datetime.datetime.strptime('2024-01-13 23:50', "%Y-%m-%d %H:%M"),
            project_id=1
        ),
        4: models.SavedTimeEntry(
            id=4,
            start_time=datetime.datetime.strptime('2024-01-14 10:00', "%Y-%m-%d %H:%M"),
            end_time=datetime.datetime.strptime('2024-01-14 13:50', "%Y-%m-%d %H:%M"),
            project_id=1
        ),
    }

    async def get_entry(self, entry_id: int) -> models.SavedTimeEntry | None:
        return self._ENTRIES.get(entry_id)

    async def save_entry(self, entry: models.TimeEntry) -> models.SavedTimeEntry:
        new_entry = models.SavedTimeEntry(
            **{
                'id': self._CUR_ID,
                **entry.dict()
            }
        )

        if new_entry.project_id and new_entry.project_id not in projects_storage.ProjectsStorage.PROJECTS:
            raise exceptions.ProjectNotFound()

        self._ENTRIES[self._CUR_ID] = new_entry
        self._CUR_ID += 1
        return new_entry

    async def get_all_entries(
            self, offset: int | None, limit: int | None, project_id: int | None
    ) -> list[models.SavedTimeEntry]:
        if project_id is not None:
            if project_id not in projects_storage.ProjectsStorage.PROJECTS:
                raise exceptions.ProjectNotFound()

            entries = [
                e
                for e in self._ENTRIES.values()
                if e.project_id == project_id
            ]
        else:
            entries = list(self._ENTRIES.values())

        entries = entries[offset or 0:]

        if limit is not None:
            entries = entries[:limit]

        return sorted(entries, key=lambda e: e.start)

    async def update_entry(self, entry_id: int, new_data: models.TimeEntry) -> models.SavedTimeEntry | None:
        if entry_id not in self._ENTRIES:
            return None

        if new_data.project_id and new_data.project_id not in projects_storage.ProjectsStorage.PROJECTS:
            raise exceptions.ProjectNotFound()

        old_data = self._ENTRIES[entry_id]
        new_data = old_data.model_copy(update=new_data.dict())

        self._ENTRIES[entry_id] = new_data
        return new_data

    async def delete_entry(self, entry_id: int) -> models.SavedTimeEntry | None:
        return self._ENTRIES.pop(entry_id, None)
