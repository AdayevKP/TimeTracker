from time_tracker.common import base_model
from time_tracker.storage import models as storage_models


class ApiBaseModel(base_model.BaseModel):
    pass


class ProjectApi(storage_models.Project):
    pass


class SavedProjectApi(storage_models.SavedProject):
    pass


class TimeEntryApi(storage_models.TimeEntry):
    pass


class SavedTimeEntryApi(storage_models.SavedTimeEntry):
    pass
