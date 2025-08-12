from typing import List

from pydantic import BaseModel

from app.schemas.activity import ActivityOut
from app.schemas.building import BuildingOut


class OrganizationBase(BaseModel):
    name: str
    building_id: int
    phones: List[str] = []


class OrganizationCreate(OrganizationBase):
    activity_ids: List[int] = []


class OrganizationOut(BaseModel):
    id: int
    name: str
    phones: List[str]
    building: BuildingOut
    activities: List[ActivityOut]

    class Config:
        from_attributes = True
