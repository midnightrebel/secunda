from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.building import Building


class BuildingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, address: str, lat: float, lon: float) -> Building:
        b = Building(address=address, lat=lat, lon=lon)
        self.session.add(b)
        await self.session.flush()
        return b

    async def get(self, building_id: int) -> Building | None:
        res = await self.session.execute(
            select(Building).where(Building.id == building_id)
        )
        return res.scalar_one_or_none()

    async def list(self, offset: int = 0, limit: int = 50):
        res = await self.session.execute(select(Building).offset(offset).limit(limit))
        return res.scalars().all()
