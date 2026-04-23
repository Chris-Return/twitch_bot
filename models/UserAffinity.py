from sqlalchemy import Integer, String, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from database import Base

class UserAffinity(Base):
    __tablename__ = "user_affinities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_users.id"), unique=True)
    
    affinity_score: Mapped[int] = mapped_column(Integer, default=0) # Amical
    respect_score: Mapped[int] = mapped_column(Integer, default=0)  # Estime
    love_score: Mapped[int] = mapped_column(Integer, default=0)     # Romantique

    last_interaction: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    user = relationship("AppUser", back_populates="affinity")

    __table_args__ = (
        CheckConstraint('affinity_score BETWEEN -100 AND 100', name='check_affinity_range'),
        CheckConstraint('respect_score BETWEEN -100 AND 100', name='check_respect_range'),
        CheckConstraint('love_score BETWEEN -100 AND 100', name='check_love_range'),
    )