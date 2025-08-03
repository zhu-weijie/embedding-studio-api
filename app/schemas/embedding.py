from typing import List

from pydantic import BaseModel


class EmbeddingBase(BaseModel):
    model_name: str
    dimensions: int
    vector: List[float]


class EmbeddingCreate(EmbeddingBase):
    pass


class Embedding(EmbeddingBase):
    id: int
    text_id: int

    model_config = {"from_attributes": True}
