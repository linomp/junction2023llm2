from typing import Optional

from pydantic import BaseModel


class Answer(BaseModel):
    answer: str
    confidence: float
    sources: list[str]


class Query(BaseModel):
    value: str


class InformationSource(BaseModel):
    url: Optional[str] = None
    title: str
    raw_content: Optional[str] = None
