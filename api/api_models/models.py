import random
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


class InformationSource(BaseModel):
    url: Optional[str] = None
    title: str
    raw_content: Optional[str] = None


class Query(BaseModel):
    question: str


@dataclass
class CoreModelAnswer:
    question: str
    answer: str
    sources: list[str]


class Answer(BaseModel):
    question: str
    answer: str
    confidence: float
    sources: list[InformationSource]

    @classmethod
    def from_core_model_answer(cls, core_model_answer: CoreModelAnswer):
        return cls(
            question=core_model_answer.question,
            answer=core_model_answer.answer,
            confidence=random.random(),
            sources=list(
                map(lambda s: InformationSource(title=s, raw_content=None, url=None), core_model_answer.sources))
        )
