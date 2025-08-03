from sqlalchemy.orm import Session

from app.models.text import Text
from app.schemas.text import TextCreate


def get_text(db: Session, text_id: int):
    return db.query(Text).filter(Text.id == text_id).first()


def create_text(db: Session, text: TextCreate):
    db_text = Text(content=text.content)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text
