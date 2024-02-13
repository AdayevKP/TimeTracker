import dataclasses
import typing as tp

import sqlalchemy as sa
from sqlalchemy import orm

from app.db import deps as db_deps
from app.db import models as orm_models
from app.storage import models


class WithId(tp.Protocol):
    id: orm.Mapped[int]


OrmObjWithIdT = tp.TypeVar('OrmObjWithIdT', bound=tp.Union[WithId, orm_models.Base])


@dataclasses.dataclass
class SAStorage:
    session: db_deps.SessionDep

    async def _update(self, model: tp.Type[OrmObjWithIdT], row_id: int, new_data: models.BaseModel) -> OrmObjWithIdT:
        query = (
            sa.update(model)
            .returning(model)
            .where(model.id == row_id)
            .values(new_data.dict(exclude_unset=True))
        )
        result = await self.session.execute(query)
        updated_data = result.scalars().first()
        await self.session.commit()
        await self.session.refresh(updated_data)

        return updated_data
