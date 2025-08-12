from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import secured_session
from app.core.config import settings
from app.core.pagination import offset_limit, page_size
from app.repositories.building_repo import BuildingRepository
from app.schemas.building import BuildingCreate, BuildingOut

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.post("", response_model=BuildingOut, status_code=201)
async def create_building(
    payload: BuildingCreate, session: AsyncSession = Depends(secured_session)
):
    repo = BuildingRepository(session)
    b = await repo.create(payload.address, payload.lat, payload.lon)
    await session.commit()
    return b


@router.get("", response_model=list[BuildingOut])
async def list_buildings(
    page: int = Query(1, ge=1),
    size: int = Query(None),
    session: AsyncSession = Depends(secured_session),
):
    size = page_size(size, settings.default_page_size, settings.max_page_size)
    offset, limit = offset_limit(page, size)
    data = await BuildingRepository(session).list(offset, limit)
    return data
