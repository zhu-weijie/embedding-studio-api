from fastapi import APIRouter

from app.api.v1.endpoints import tokenizer

api_router = APIRouter()
api_router.include_router(tokenizer.router, prefix="/v1", tags=["Tokenizer"])
