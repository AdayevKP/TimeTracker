from app import models


class ProjectsStorage:
    _CUR_PROJ_ID = 4
    _PROJECTS = {
        1: models.SavedProject(
            id=1, name="work"
        ),
        2: models.SavedProject(
            id=2, name="study"
        ),
        3: models.SavedProject(
            id=3, name="sport", description='lifting weights'
        ),
    }

    async def get_project(self, proj_id: int) -> models.SavedProject | None:
        return self._PROJECTS.get(proj_id)

    async def save_project(self, proj: models.Project) -> models.SavedProject:
        new_proj = models.SavedProject(
            **{
                'id': self._CUR_PROJ_ID,
                **proj.dict()
            }
        )
        self._PROJECTS[self._CUR_PROJ_ID] = new_proj
        self._CUR_PROJ_ID += 1
        return new_proj

    async def get_all_projects(self) -> list[models.SavedProject]:
        return list(self._PROJECTS.values())

    async def update_project(
            self, proj_id: int, new_data: models.Project
    ) -> models.SavedProject | None:
        if proj_id not in self._PROJECTS:
            return None

        old_data = self._PROJECTS[proj_id]
        new_data = old_data.model_copy(update=new_data.dict())
        self._PROJECTS[proj_id] = new_data
        return new_data

