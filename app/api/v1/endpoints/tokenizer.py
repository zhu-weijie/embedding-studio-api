import tiktoken
from fastapi import APIRouter

from app.schemas.tokenizer import TokenizeRequest, TokenizeResponse

router = APIRouter()
tokenizer = tiktoken.get_encoding("gpt2")


@router.post("/tokenize", response_model=TokenizeResponse)
def tokenize_text(request: TokenizeRequest) -> TokenizeResponse:
    token_ids = tokenizer.encode(request.text)
    return TokenizeResponse(tokens=token_ids)
