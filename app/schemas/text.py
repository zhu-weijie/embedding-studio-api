from datetime import datetime

from pydantic import BaseModel


class TextBase(BaseModel):
    content: str


class TextCreate(TextBase):
    pass


class Text(TextBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
