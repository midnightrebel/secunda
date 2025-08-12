from fastapi import Header, HTTPException, status

from app.core.config import settings


async def api_key_auth(x_api_key: str = Header(None, alias="X-API-Key")):
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )
    return True
