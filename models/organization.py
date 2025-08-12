from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="RESTRICT"), index=True
    )

    building = relationship("Building", back_populates="organizations")
    phones = relationship(
        "OrganizationPhone", back_populates="organization", cascade="all, delete-orphan"
    )
    activities = relationship(
        "Activity", secondary="organization_activities", back_populates="organizations"
    )


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    phone: Mapped[str] = mapped_column(String(32), index=True)

    organization = relationship("Organization", back_populates="phones")
