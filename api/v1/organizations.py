from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import secured_session
from app.core.config import settings
from app.core.pagination import offset_limit, page_size
from app.repositories.activity_repo import ActivityRepository
from app.repositories.organization_repo import OrganizationRepository
from app.schemas.organization import OrganizationCreate, OrganizationOut
from app.services.geo import normalize_bounds

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("", response_model=OrganizationOut, status_code=201)
async def create_organization(
    payload: OrganizationCreate, session: AsyncSession = Depends(secured_session)
):
    org_repo = OrganizationRepository(session)
    act_repo = ActivityRepository(session)
    org = await org_repo.create(
        payload.name, payload.building_id, payload.phones, payload.activity_ids
    )
    await session.commit()
    org = await org_repo.get(org.id)
    return to_org_out(org)


@router.get("/{org_id}", response_model=OrganizationOut)
async def get_organization(
    org_id: int, session: AsyncSession = Depends(secured_session)
):
    org = await OrganizationRepository(session).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return to_org_out(org)


@router.get("", response_model=list[OrganizationOut])
async def list_organizations_by_filters(
    building_id: int | None = None,
    activity_id: int | None = None,
    name: str | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(None),
    session: AsyncSession = Depends(secured_session),
):
    size = page_size(size, settings.default_page_size, settings.max_page_size)
    offset, limit = offset_limit(page, size)
    repo = OrganizationRepository(session)
    if building_id is not None:
        data = await repo.list_by_building(building_id, offset, limit)
    elif activity_id is not None:
        acts = await ActivityRepository(session).list_children_ids_recursive(
            activity_id
        )
        data = await repo.list_by_activities(acts, offset, limit)
    elif name:
        data = await repo.search_by_name(name, offset, limit)
    else:
        # fallback: list all
        data = await repo.search_by_name("", offset, limit)
    return [to_org_out(o) for o in data]


@router.get("/geo/rectangle", response_model=list[OrganizationOut])
async def organizations_in_rectangle(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    page: int = Query(1, ge=1),
    size: int = Query(None),
    session: AsyncSession = Depends(secured_session),
):
    size = page_size(size, settings.default_page_size, settings.max_page_size)
    offset, limit = offset_limit(page, size)
    min_lat, min_lon, max_lat, max_lon = normalize_bounds(lat1, lon1, lat2, lon2)
    data = await OrganizationRepository(session).list_in_rectangle(
        min_lat, min_lon, max_lat, max_lon, offset, limit
    )
    return [to_org_out(o) for o in data]


@router.get("/geo/radius", response_model=list[OrganizationOut])
async def organizations_in_radius(
    lat: float,
    lon: float,
    radius_m: float = Query(..., gt=0, le=50_000),
    page: int = Query(1, ge=1),
    size: int = Query(None),
    session: AsyncSession = Depends(secured_session),
):
    size = page_size(size, settings.default_page_size, settings.max_page_size)
    offset, limit = offset_limit(page, size)
    data = await OrganizationRepository(session).list_in_radius(
        lat, lon, radius_m, offset, limit
    )
    return [to_org_out(o) for o in data]


def to_org_out(org) -> OrganizationOut:
    return OrganizationOut(
        id=org.id,
        name=org.name,
        phones=[p.phone for p in org.phones],
        building=org.building,
        activities=org.activities,
    )
