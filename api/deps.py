from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.security import api_key_auth


async def secured_session(
    _: bool = Depends(api_key_auth), session: AsyncSession = Depends(get_session)
):
    return session
