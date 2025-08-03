from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud_embedding, crud_text
from app.db.session import SessionLocal
from app.services.bedrock import bedrock_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/texts", response_model=schemas.Text)
def create_text(text: schemas.TextCreate, db: Session = Depends(get_db)):
    return crud_text.create_text(db=db, text=text)


@router.post("/texts/{text_id}/embeddings", response_model=schemas.Embedding)
def create_embedding_for_text(text_id: int, db: Session = Depends(get_db)):
    db_text = crud_text.get_text(db, text_id=text_id)
    if db_text is None:
        raise HTTPException(status_code=404, detail="Text not found")

    vector = bedrock_service.generate_embedding(text=db_text.content)

    embedding_data = schemas.EmbeddingCreate(
        model_name="amazon.titan-embed-text-v2:0", dimensions=len(vector), vector=vector
    )

    return crud_embedding.create_text_embedding(
        db=db, embedding=embedding_data, text_id=text_id
    )
