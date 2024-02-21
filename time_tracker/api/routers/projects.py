import fastapi as fa

from time_tracker.api import context as ctx
from time_tracker.api import models


router = fa.APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("/", status_code=fa.status.HTTP_201_CREATED)
async def add_project(
    context: ctx.ApiContextDep, project: models.ProjectApi
) -> models.SavedProjectApi:
    return await context.proj_storage.save_project(project)


@router.get("/", status_code=fa.status.HTTP_200_OK)
async def get_projects_list(
    context: ctx.ApiContextDep,
) -> list[models.SavedProjectApi]:
    return await context.proj_storage.get_all_projects()


@router.get("/{project_id}", status_code=fa.status.HTTP_200_OK)
async def get_project(
    context: ctx.ApiContextDep, project_id: int
) -> models.SavedProjectApi:
    proj = await context.proj_storage.get_project(project_id)

    if proj is None:
        raise fa.HTTPException(
            status_code=404, detail=f"Project {project_id} not found"
        )

    return proj


@router.put("/{project_id}", status_code=fa.status.HTTP_200_OK)
async def update_project(
    context: ctx.ApiContextDep, project_id: int, project: models.ProjectApi
) -> models.SavedProjectApi:
    proj = await context.proj_storage.update_project(project_id, project)

    if proj is None:
        raise fa.HTTPException(
            status_code=404, detail=f"Project {project_id} not found"
        )

    return proj
