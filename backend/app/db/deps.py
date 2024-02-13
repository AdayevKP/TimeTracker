import typing as tp

import fastapi as fa
from sqlalchemy.ext import asyncio as sa

from app.db import database


async def _get_session():
    async with database.AsyncSessionLocal() as sess:
        yield sess


SessionDep = tp.Annotated[sa.AsyncSession, fa.Depends(_get_session)]
