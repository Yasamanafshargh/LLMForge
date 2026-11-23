from pydantic import BaseModel, Field
from typing import Any


class Document(BaseModel):

    id: str

    text: str

    metadata: dict[str, Any] = Field(default_factory=dict)

    tokens: list[str] = Field(default_factory=list)

    token_ids: list[int] = Field(default_factory=list)