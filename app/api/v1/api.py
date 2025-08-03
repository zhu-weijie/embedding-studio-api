from fastapi import APIRouter

from app.api.v1.endpoints import search, texts, tokenizer

api_router = APIRouter()
api_router.include_router(tokenizer.router, prefix="/v1", tags=["Tokenizer"])
api_router.include_router(texts.router, prefix="/v1", tags=["Texts & Embeddings"])
api_router.include_router(search.router, prefix="/v1", tags=["Search"])
