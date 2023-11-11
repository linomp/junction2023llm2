from typing import Union

from pydantic import BaseModel


class Answer(BaseModel):
    answer: str
    confidence: float
    sources: list[str]


class Query(BaseModel):
    value: str


class InformationSource(BaseModel):
    url: Union[str, None]
    title: str
    raw_content: Union[str, None]
