import typing as tp

import fastapi as fa

from time_tracker.api import context as ctx
from time_tracker.storage import exceptions as storage_exc
from time_tracker.storage import models


router = fa.APIRouter(
    prefix="/time_entries",
    tags=["time_entries"],
)


@router.post("/")
async def add_entry(
    context: ctx.ApiContextDep, entry: models.TimeEntry
) -> models.SavedTimeEntry:
    try:
        return await context.entries_storage.save_entry(entry)
    except storage_exc.ProjectNotFound:
        raise fa.HTTPException(
            status_code=400, detail=f"Project {entry.project_id} not found"
        )


@router.get("/")
async def get_entries_list(
    context: ctx.ApiContextDep,
    project_id: int | None = None,
    offset: int = 0,
    limit: tp.Annotated[int, fa.Query(le=100)] = 20,
) -> list[models.SavedTimeEntry]:
    try:
        return await context.entries_storage.get_all_entries(
            offset, limit, project_id
        )
    except storage_exc.ProjectNotFound:
        raise fa.HTTPException(
            status_code=400, detail=f"Project {project_id} not found"
        )


@router.get("/{entry_id}")
async def get_entry(
    context: ctx.ApiContextDep, entry_id: int
) -> models.SavedTimeEntry:
    entry = await context.entries_storage.get_entry(entry_id)

    if entry is None:
        raise fa.HTTPException(
            status_code=404, detail=f"Time Entry {entry_id} not found"
        )

    return entry


@router.put("/{entry_id}")
async def update_entry(
    context: ctx.ApiContextDep, entry_id: int, entry: models.TimeEntry
) -> models.SavedTimeEntry:
    try:
        updated_entry = await context.entries_storage.update_entry(
            entry_id, entry
        )
    except storage_exc.ProjectNotFound:
        raise fa.HTTPException(
            status_code=400, detail=f"Project {entry.project_id} not found"
        )

    if updated_entry is None:
        raise fa.HTTPException(
            status_code=404, detail=f"Time Entry {entry_id} not found"
        )

    return updated_entry


@router.delete("/{entry_id}")
async def delete_entry(
    context: ctx.ApiContextDep, entry_id: int
) -> models.SavedTimeEntry:
    deleted_entry = await context.entries_storage.delete_entry(entry_id)

    if deleted_entry is None:
        raise fa.HTTPException(
            status_code=404, detail=f"Time Entry {entry_id} not found"
        )

    return deleted_entry
