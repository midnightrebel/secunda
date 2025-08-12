from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        UniqueConstraint("name", "parent_id", name="uq_activity_name_parent"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), nullable=True
    )
    level: Mapped[int] = mapped_column(default=1, nullable=False)  # 1..3

    parent = relationship("Activity", remote_side="Activity.id", backref="children")
    organizations = relationship(
        "Organization", secondary="organization_activities", back_populates="activities"
    )
