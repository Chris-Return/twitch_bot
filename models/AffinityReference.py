from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class AffinityReference(Base):
    __tablename__ = "affinity_references"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # 'affinity', 'respect', ou 'love'
    category: Mapped[str] = mapped_column(String, nullable=False) 
    
    min_score: Mapped[int] = mapped_column(Integer, nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Le libellé (ex: "IDÔLE", "RIVAL", "FLIRT")
    label: Mapped[str] = mapped_column(String, nullable=False)
    
    # Une directive comportementale pour aider l'IA
    instruction: Mapped[str] = mapped_column(String, nullable=True)