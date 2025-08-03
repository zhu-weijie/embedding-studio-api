from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import crud_embedding
from app.schemas.text import Text
from app.schemas.tokenizer import TokenizeRequest
from app.services.bedrock import bedrock_service

router = APIRouter()


@router.post("/search", response_model=List[Text])
def search_for_texts(search_query: TokenizeRequest, db: Session = Depends(get_db)):
    query_vector = bedrock_service.generate_embedding(text=search_query.text)

    search_results = crud_embedding.search_similar_texts(
        db=db, query_vector=query_vector
    )

    if not search_results:
        return []

    return [result[0] for result in search_results]
