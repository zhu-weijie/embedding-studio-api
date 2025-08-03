from typing import List

from sqlalchemy.orm import Session

from app.models.embedding import Embedding
from app.models.text import Text
from app.schemas.embedding import EmbeddingCreate


def create_text_embedding(db: Session, embedding: EmbeddingCreate, text_id: int):
    db_embedding = Embedding(**embedding.model_dump(), text_id=text_id)
    db.add(db_embedding)
    db.commit()
    db.refresh(db_embedding)
    return db_embedding


def search_similar_texts(db: Session, query_vector: List[float], limit: int = 5):
    results = (
        db.query(Text, Embedding.vector.cosine_distance(query_vector).label("distance"))
        .join(Embedding)
        .order_by("distance")
        .limit(limit)
        .all()
    )

    return results
