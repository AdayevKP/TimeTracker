import fastapi as fa
import typing as tp

from app import models

router = fa.APIRouter(
    prefix="/time_entries",
    tags=["time_entries"],
    responses={404: {"description": "Not found"}},
)


@router.post('/')
async def add_entry(entry: models.TimeEntry):
    return {'id': 1, **entry.dict()}


@router.get('/')
async def get_entries_list(
        project_id: int | None,
        offset: int = 0,
        limit: tp.Annotated[int, fa.Query(le=100)] = 20
):
    return [{'id': 1}, {'id': 2}]


@router.get('/{id}')
async def get_entry(entry_id: int):
    return {'id': entry_id}


@router.put('/{id}')
async def update_entry(entry_id: int, entry: models.TimeEntry):
    return {'id': entry_id, **entry.dict()}


@router.delete('/{id}')
async def delete_entry(entry_id: int):
    return {'id': entry_id}
