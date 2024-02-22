import typing as tp

import fastapi as fa
from sqlalchemy.ext import asyncio as sa

from time_tracker.db import database


async def get_session() -> tp.AsyncGenerator[sa.AsyncSession, None]:
    async with database.AsyncSessionLocal() as sess:
        yield sess


def get_session_factory() -> tp.Generator[
    database.AsyncSessionLocal, None, None
]:
    yield database.AsyncSessionLocal


SessionDep = tp.Annotated[sa.AsyncSession, fa.Depends(get_session)]
SessionFactoryDep = tp.Annotated[
    database.AsyncSessionLocal, fa.Depends(get_session_factory)
]
