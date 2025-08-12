from fastapi import FastAPI

from app.api.v1.activities import router as a_router
from app.api.v1.buildings import router as b_router
from app.api.v1.organizations import router as org_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(org_router, prefix=settings.api_v1_prefix)
app.include_router(b_router, prefix=settings.api_v1_prefix)
app.include_router(a_router, prefix=settings.api_v1_prefix)
