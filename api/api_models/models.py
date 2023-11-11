from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


class InformationSource(BaseModel):
    url: Optional[str] = None
    title: str
    raw_content: Optional[str] = None


class Answer(BaseModel):
    question: str
    answer: str
    confidence: float
    sources: list[InformationSource]


class Query(BaseModel):
    question: str


@dataclass
class CoreModelAnswer:
    question: str
    answer: str
    sources: list[str]
