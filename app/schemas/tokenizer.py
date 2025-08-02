from typing import List

from pydantic import BaseModel


class TokenizeRequest(BaseModel):
    text: str


class TokenizeResponse(BaseModel):
    tokens: List[int]
    model: str = "gpt2"
