from sqlalchemy.orm import Session

from app.models.embedding import Embedding
from app.schemas.embedding import EmbeddingCreate


def create_text_embedding(db: Session, embedding: EmbeddingCreate, text_id: int):
    db_embedding = Embedding(**embedding.model_dump(), text_id=text_id)
    db.add(db_embedding)
    db.commit()
    db.refresh(db_embedding)
    return db_embedding
