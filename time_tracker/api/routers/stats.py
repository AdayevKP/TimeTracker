import datetime

import fastapi as fa

from time_tracker.api import models
from time_tracker.storage import stats_storage
from time_tracker.utils import time_intervals


router = fa.APIRouter(
    prefix="/statistics",
    tags=["statistics"],
)


@router.post("/", status_code=fa.status.HTTP_200_OK)
async def get_stats(
    storage: stats_storage.StatsStorageDep, req: models.StatsRequestApi
) -> models.StatsResponseApi:
    start_date, end_date = time_intervals.get_date_bounds(req.scale.value)

    end = datetime.datetime.combine(
        end_date + datetime.timedelta(days=1), datetime.datetime.min.time()
    )
    start = datetime.datetime.combine(start_date, datetime.datetime.min.time())
    stats = await storage.get_full_time_stats(start, end)

    return models.StatsResponseApi(
        total_time=stats.total_time,
        time_per_project=[
            models.ProjectTime(project_id=p, time=t)
            for p, t in stats.time_per_project
        ],
        time_per_day={
            str(d): stats.time_per_day.get(d, datetime.timedelta())
            for d in time_intervals.get_all_dates_in_scale(req.scale.value)
        },
    )
