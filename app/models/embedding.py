from sqlalchemy import ARRAY, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True)
    text_id = Column(Integer, ForeignKey("texts.id"), nullable=False)
    model_name = Column(String(100), nullable=False)
    dimensions = Column(Integer, nullable=False)
    vector = Column(ARRAY(Float), nullable=False)

    text = relationship("Text", back_populates="embeddings")
