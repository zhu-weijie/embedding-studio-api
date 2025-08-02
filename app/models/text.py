from sqlalchemy import TIMESTAMP, Column, Integer, Text, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Text(Base):
    __tablename__ = "texts"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    embeddings = relationship(
        "Embedding", back_populates="text", cascade="all, delete-orphan"
    )
