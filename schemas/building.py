from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    address: str
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)


class BuildingCreate(BuildingBase):
    pass


class BuildingOut(BuildingBase):
    id: int

    class Config:
        from_attributes = True
