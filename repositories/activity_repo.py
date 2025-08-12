from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.activity import Activity


class ActivityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, activity_id: int) -> Activity | None:
        res = await self.session.execute(
            select(Activity).where(Activity.id == activity_id)
        )
        return res.scalar_one_or_none()

    async def create(self, name: str, parent_id: int | None) -> Activity:
        level = 1
        if parent_id:
            parent = await self.get(parent_id)
            if not parent:
                raise ValueError("Parent activity not found")
            level = parent.level + 1
        if level > settings.max_activity_levels:
            raise ValueError(f"Max activity levels is {settings.max_activity_levels}")
        act = Activity(name=name, parent_id=parent_id, level=level)
        self.session.add(act)
        await self.session.flush()
        return act

    async def list_children_ids_recursive(self, root_id: int) -> list[int]:
        ids = [root_id]
        frontier = [root_id]
        for _ in range(settings.max_activity_levels - 1):
            if not frontier:
                break
            q = select(Activity.id).where(Activity.parent_id.in_(frontier))
            res = await self.session.execute(q)
            next_ids = [r[0] for r in res.all()]
            frontier = next_ids
            ids.extend(next_ids)
        return list(dict.fromkeys(ids))
