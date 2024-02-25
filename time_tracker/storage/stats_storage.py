import asyncio
import dataclasses
import datetime
import typing as tp

import fastapi as fa
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.sql import expression as ex
from sqlalchemy.sql import functions as func

from time_tracker.db import deps as db_deps
from time_tracker.db import models as tbl
from time_tracker.storage import common


ProjectId = int | None
TimePerProject = list[tuple[ProjectId, datetime.timedelta]]
TimePerDay = dict[datetime.date, datetime.timedelta]


class FullStats(tp.NamedTuple):
    total_time: datetime.timedelta
    time_per_project: TimePerProject
    time_per_day: TimePerDay


def _min(a: orm.Mapped[tp.Any], b: tp.Any) -> sa.Case[tp.Any]:
    return ex.case((a > b, b), else_=a)


def _max(a: orm.Mapped[tp.Any], b: tp.Any) -> sa.Case[tp.Any]:
    return ex.case((a > b, a), else_=b)


@dataclasses.dataclass
class StatsStorage(common.SAStorage):
    session_factory: db_deps.SessionFactoryDep

    async def _get_total_time(
        self, start: datetime.datetime, end: datetime.datetime
    ) -> datetime.timedelta:
        query = (
            sa.select(
                func.sum(
                    _min(tbl.TimeEntry.end_time, end)
                    - _max(tbl.TimeEntry.start_time, start)
                )
            )
            .filter(
                tbl.TimeEntry.start_time.between(start, end)
                | tbl.TimeEntry.end_time.between(start, end)
            )
            .filter(tbl.TimeEntry.end_time.is_not(None))
        )

        async with self.session_factory() as session:
            res = await session.execute(query)

        total_time = res.scalars().first()
        return total_time or datetime.timedelta()

    async def _get_time_per_project(
        self, start: datetime.datetime, end: datetime.datetime
    ) -> TimePerProject:
        query = (
            sa.select(
                tbl.TimeEntry.project_id,
                func.sum(
                    _min(tbl.TimeEntry.end_time, end)
                    - _max(tbl.TimeEntry.start_time, start)
                ),
            )
            .filter(
                tbl.TimeEntry.start_time.between(start, end)
                | tbl.TimeEntry.end_time.between(start, end)
            )
            .filter(tbl.TimeEntry.end_time.is_not(None))
            .group_by(tbl.TimeEntry.project_id)
            .order_by(tbl.TimeEntry.project_id)
        )

        async with self.session_factory() as session:
            res = await session.execute(query)

        time_per_project = res.fetchall()
        return time_per_project

    async def _get_time_per_day(
        self, start: datetime.datetime, end: datetime.datetime
    ) -> TimePerDay:
        time_by_start = (
            sa.select(
                sa.cast(_max(tbl.TimeEntry.start_time, start), sa.Date).label(
                    "start_date"
                ),
                (
                    _min(tbl.TimeEntry.end_time, end)
                    - _max(tbl.TimeEntry.start_time, start)
                ).label("time"),
            )
            .filter(
                tbl.TimeEntry.start_time.between(start, end)
                | tbl.TimeEntry.end_time.between(start, end)
            )
            .filter(tbl.TimeEntry.end_time.is_not(None))
            .subquery()
        )

        query = sa.select(
            time_by_start.c.start_date, func.sum(time_by_start.c.time)
        ).group_by(time_by_start.c.start_date)

        async with self.session_factory() as session:
            res = await session.execute(query)

        time_per_day = res.fetchall()
        return {d: t for d, t in time_per_day}

    async def get_full_time_stats(
        self, start: datetime.datetime, end: datetime.datetime
    ) -> FullStats:
        res = await asyncio.gather(
            self._get_total_time(start, end),
            self._get_time_per_project(start, end),
            self._get_time_per_day(start, end),
        )
        return FullStats(*res)


StatsStorageDep = tp.Annotated[StatsStorage, fa.Depends()]
