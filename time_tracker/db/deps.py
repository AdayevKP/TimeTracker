import typing as tp

import fastapi as fa
from sqlalchemy.ext import asyncio as sa

from time_tracker.db import database


async def _get_session() -> tp.AsyncGenerator[sa.AsyncSession, None]:
    async with database.AsyncSessionLocal() as sess:
        yield sess


SessionDep = tp.Annotated[sa.AsyncSession, fa.Depends(_get_session)]
