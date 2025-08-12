from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import secured_session
from app.repositories.activity_repo import ActivityRepository
from app.schemas.activity import ActivityCreate, ActivityOut

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("", response_model=ActivityOut, status_code=201)
async def create_activity(
    payload: ActivityCreate, session: AsyncSession = Depends(secured_session)
):
    repo = ActivityRepository(session)
    try:
        act = await repo.create(payload.name, payload.parent_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await session.commit()
    return act


@router.get("/{activity_id}/subtree", response_model=list[int])
async def get_subtree_ids(
    activity_id: int, session: AsyncSession = Depends(secured_session)
):
    repo = ActivityRepository(session)
    ids = await repo.list_children_ids_recursive(activity_id)
    return ids
