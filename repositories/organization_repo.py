from math import asin
from math import cos
from math import cos as mcos
from math import radians
from math import radians as rad
from math import sin, sqrt

from sqlalchemy import and_, func, literal, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.associations import OrganizationActivity
from app.models.building import Building
from app.models.organization import Organization, OrganizationPhone
from app.repositories.const import LENGTH_MINUTE, R


class OrganizationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, name: str, building_id: int, phones: list[str], activity_ids: list[int]
    ) -> Organization:
        org = Organization(name=name, building_id=building_id)
        self.session.add(org)
        await self.session.flush()
        if phones:
            self.session.add_all(
                [OrganizationPhone(organization_id=org.id, phone=p) for p in phones]
            )
        if activity_ids:
            self.session.add_all(
                [
                    OrganizationActivity(organization_id=org.id, activity_id=a)
                    for a in activity_ids
                ]
            )
        await self.session.flush()
        return org

    async def get(self, org_id: int) -> Organization | None:
        q = (
            select(Organization)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities),
                joinedload(Organization.phones),
            )
            .where(Organization.id == org_id)
        )
        res = await self.session.execute(q)
        return res.scalar_one_or_none()

    async def list_by_building(self, building_id: int, offset: int, limit: int):
        q = (
            select(Organization)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities),
                joinedload(Organization.phones),
            )
            .where(Organization.building_id == building_id)
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(q)
        return res.scalars().all()

    async def list_by_activities(
        self, activity_ids: list[int], offset: int, limit: int
    ):
        q = (
            select(Organization)
            .join(
                OrganizationActivity,
                OrganizationActivity.organization_id == Organization.id,
            )
            .where(OrganizationActivity.activity_id.in_(activity_ids))
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities),
                joinedload(Organization.phones),
            )
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(q)
        return res.scalars().all()

    async def search_by_name(self, query: str, offset: int, limit: int):
        pattern = f"%{query.lower()}%"
        q = (
            select(Organization)
            .where(func.lower(Organization.name).like(pattern))
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones),
            )
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(q)
        return res.scalars().unique().all()

    async def list_in_rectangle(
        self,
        min_lat: float,
        min_lon: float,
        max_lat: float,
        max_lon: float,
        offset: int,
        limit: int,
    ):
        q = (
            select(Organization)
            .join(Building, Building.id == Organization.building_id)
            .where(
                and_(
                    Building.lat >= min_lat,
                    Building.lat <= max_lat,
                    Building.lon >= min_lon,
                    Building.lon <= max_lon,
                )
            )
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities),
                joinedload(Organization.phones),
            )
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(q)
        return res.scalars().all()

    async def list_in_radius(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float,
        offset: int,
        limit: int,
    ):
        deg_lat = radius_m / LENGTH_MINUTE
        deg_lon = radius_m / (LENGTH_MINUTE * max(0.1, cos(radians(center_lat))))
        min_lat, max_lat = center_lat - deg_lat, center_lat + deg_lat
        min_lon, max_lon = center_lon - deg_lon, center_lon + deg_lon

        q = (
            select(Organization)
            .join(Building, Building.id == Organization.building_id)
            .where(
                and_(
                    Building.lat >= min_lat,
                    Building.lat <= max_lat,
                    Building.lon >= min_lon,
                    Building.lon <= max_lon,
                )
            )
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities),
                joinedload(Organization.phones),
            )
        )
        res = await self.session.execute(q)
        candidates = res.scalars().unique().all()

        filtered = []
        for org in candidates:
            d = self._haversine(
                org.building.lat, org.building.lon, center_lat, center_lon
            )
            if d <= radius_m:
                filtered.append(org)
        return filtered[offset : offset + limit]

    @staticmethod
    def _haversine(lat: float, lon: float, center_lat: float, center_lon: float):
        dlat = rad(lat - center_lat)
        dlon = rad(lon - center_lon)
        a = (
            sin(dlat / 2) ** 2
            + mcos(rad(center_lat)) * mcos(rad(lat)) * sin(dlon / 2) ** 2
        )
        return 2 * R * asin(sqrt(a))
