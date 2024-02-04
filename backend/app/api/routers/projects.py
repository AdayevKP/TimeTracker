import fastapi as fa
import typing as tp

from app.api import models


router = fa.APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.post('/')
async def add_project(project: models.Project):
    return {'id': 1, **project.dict()}


@router.get('/')
async def get_projects_list(offset: int = 0, limit: tp.Annotated[int, fa.Query(le=100)] = 20):
    return [{'id': 1}, {'id': 2}]


@router.get('/{project_id}')
async def get_project(project_id: int):
    return {'id': project_id}


@router.put('/{project_id}')
async def update_project(project_id: int, project: models.Project):
    return {'id': project_id, **project.dict()}
