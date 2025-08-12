from pydantic import BaseModel, Field


class ActivityBase(BaseModel):
    name: str
    parent_id: int | None = None


class ActivityCreate(ActivityBase):
    pass


class ActivityOut(BaseModel):
    id: int
    name: str
    parent_id: int | None
    level: int

    class Config:
        from_attributes = True
