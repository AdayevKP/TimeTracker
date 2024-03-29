import typing as tp

import fastapi as fa

from time_tracker.api import context as ctx
from time_tracker.api import models
from time_tracker.storage import exceptions as storage_exc


router = fa.APIRouter(
    prefix="/time_entries",
    tags=["time_entries"],
)


@router.post("/", status_code=fa.status.HTTP_201_CREATED)
async def add_entry(
    context: ctx.ApiContextDep, entry: models.TimeEntryApi
) -> models.SavedTimeEntryApi:
    try:
        return await context.entries_storage.save_entry(entry)
    except storage_exc.ProjectNotFound:
        raise fa.HTTPException(
            status_code=400, detail=f"Project {entry.project_id} not found"
        )


@router.get("/", status_code=fa.status.HTTP_200_OK)
async def get_entries_list(
    context: ctx.ApiContextDep,
    project_id: int | None = None,
    offset: int = 0,
    limit: tp.Annotated[int, fa.Query(le=100)] = 20,
) -> list[models.SavedTimeEntryApi]:
    try:
        return await context.entries_storage.get_all_entries(
            offset, limit, project_id
        )
    except storage_exc.ProjectNotFound:
        raise fa.HTTPException(
            status_code=400, detail=f"Project {project_id} not found"
        )


@router.get("/{entry_id}", status_code=fa.status.HTTP_200_OK)
async def get_entry(
    context: ctx.ApiContextDep, entry_id: int
) -> models.SavedTimeEntryApi:
    entry = await context.entries_storage.get_entry(entry_id)

    if entry is None:
        raise fa.HTTPException(
            status_code=404, detail=f"Time Entry {entry_id} not found"
        )

    return entry


@router.put("/{entry_id}", status_code=fa.status.HTTP_200_OK)
async def update_entry(
    context: ctx.ApiContextDep, entry_id: int, entry: models.TimeEntryApi
) -> models.SavedTimeEntryApi:
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


@router.delete("/{entry_id}", status_code=fa.status.HTTP_200_OK)
async def delete_entry(
    context: ctx.ApiContextDep, entry_id: int
) -> models.SavedTimeEntryApi:
    deleted_entry = await context.entries_storage.delete_entry(entry_id)

    if deleted_entry is None:
        raise fa.HTTPException(
            status_code=404, detail=f"Time Entry {entry_id} not found"
        )

    return deleted_entry
