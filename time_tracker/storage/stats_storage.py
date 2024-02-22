import asyncio
import dataclasses
import datetime
import typing as tp

import fastapi as fa
import sqlalchemy as sa
from sqlalchemy.sql import functions as func

from time_tracker.db import deps as db_deps
from time_tracker.db import models as orm
from time_tracker.storage import common


ProjectId = int | None
TimePerProject = list[tuple[ProjectId, datetime.timedelta]]
TimePerDay = dict[datetime.date, datetime.timedelta]


class FullStats(tp.NamedTuple):
    total_time: datetime.timedelta
    time_per_project: TimePerProject
    time_per_day: TimePerDay


@dataclasses.dataclass
class StatsStorage(common.SAStorage):
    session_factory: db_deps.SessionFactoryDep

    async def _get_total_time(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> datetime.timedelta:
        async with self.session_factory() as session:
            query = await session.execute(
                sa.select(
                    func.sum(orm.TimeEntry.end_time - orm.TimeEntry.start_time)
                )
                .filter(orm.TimeEntry.end_time <= end_date)
                .filter(orm.TimeEntry.start_time >= start_date)
            )
        total_time = query.scalars().first()
        return total_time

    async def _get_time_per_project(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> TimePerProject:
        async with self.session_factory() as session:
            query = await session.execute(
                sa.select(
                    orm.TimeEntry.project_id,
                    func.sum(
                        orm.TimeEntry.end_time - orm.TimeEntry.start_time
                    ),
                )
                .filter(orm.TimeEntry.end_time <= end_date)
                .filter(orm.TimeEntry.start_time >= start_date)
                .group_by(orm.TimeEntry.project_id)
            )

        time_per_project = query.fetchall()
        return time_per_project

    async def _get_time_per_day(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> TimePerDay:
        async with self.session_factory() as session:
            query = await session.execute(
                sa.select(
                    sa.cast(orm.TimeEntry.start_time, sa.Date),
                    func.sum(
                        orm.TimeEntry.end_time - orm.TimeEntry.start_time
                    ),
                )
                .filter(orm.TimeEntry.end_time <= end_date)
                .filter(orm.TimeEntry.start_time >= start_date)
                .group_by(sa.cast(orm.TimeEntry.start_time, sa.Date))
            )

        time_per_day = query.fetchall()
        return {d: t for d, t in time_per_day}

    async def get_full_time_stats(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> FullStats:
        res = await asyncio.gather(
            self._get_total_time(start_date, end_date),
            self._get_time_per_project(start_date, end_date),
            self._get_time_per_day(start_date, end_date),
        )
        return FullStats(*res)


StatsStorageDep = tp.Annotated[StatsStorage, fa.Depends()]
